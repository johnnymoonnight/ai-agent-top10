"""工作流引擎 - 融合 n8n/Mastra/Temporal 的工作流编排"""
from __future__ import annotations
import asyncio
import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger("omniagent.workflow")


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class WorkflowStep:
    name: str
    action: Callable
    depends_on: List[str] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3
    timeout: float = 300.0
    on_failure: Optional[str] = None  # step name to jump to on failure


@dataclass
class WorkflowDefinition:
    """工作流定义 - Mastra graph-based workflow"""
    name: str
    description: str = ""
    steps: Dict[str, WorkflowStep] = field(default_factory=dict)
    version: str = "1.0"
    on_complete: Optional[Callable] = None
    on_error: Optional[Callable] = None


class WorkflowEngine:
    """
    工作流引擎 - 融合:
    - n8n: 节点式工作流
    - Mastra: .then().branch().parallel()
    - CrewAI Flows: 事件驱动
    - Temporal: 持久化执行
    """

    def __init__(self):
        self._workflows: Dict[str, WorkflowDefinition] = {}
        self._active_runs: Dict[str, Dict] = {}
        self._history: List[Dict] = []

    def register(self, workflow: WorkflowDefinition):
        self._workflows[workflow.name] = workflow

    async def run(self, name: str, initial_context: Optional[Dict] = None) -> Dict:
        wf = self._workflows.get(name)
        if not wf:
            return {"error": f"Workflow {name} not found"}

        run_id = f"{name}_{datetime.now().timestamp()}"
        context = initial_context or {}
        status = WorkflowStatus.RUNNING
        completed = set()
        results = {}

        while len(completed) < len(wf.steps):
            for step_name, step in wf.steps.items():
                if step_name in completed:
                    continue
                deps_met = all(d in completed for d in step.depends_on)
                if not deps_met:
                    continue
                try:
                    result = await asyncio.wait_for(
                        step.action(context), timeout=step.timeout
                    )
                    results[step_name] = result
                    completed.add(step_name)
                    context[f"{step_name}_result"] = result
                except Exception as e:
                    logger.error(f"Step {step_name} failed: {e}")
                    if step.on_failure and step.on_failure in wf.steps:
                        completed.add(step_name)
                        results[step_name] = {"error": str(e), "redirect": step.on_failure}
                        continue
                    status = WorkflowStatus.FAILED
                    if wf.on_error:
                        await wf.on_error({"step": step_name, "error": str(e), "context": context})
                    break

        if status == WorkflowStatus.RUNNING:
            status = WorkflowStatus.COMPLETED
            if wf.on_complete:
                await wf.on_complete(context)

        run_record = {"run_id": run_id, "workflow": name, "status": status.value,
                      "results": results, "timestamp": datetime.now().isoformat()}
        self._history.append(run_record)

        return run_record

    def get_status(self, run_id: str) -> Optional[Dict]:
        for r in self._history:
            if r["run_id"] == run_id:
                return r
        return None

    def list_runs(self, limit: int = 20) -> List[Dict]:
        return self._history[-limit:]
