"""核心基类 - 融合 AutoGPT 自主性与 CrewAI 角色定义"""
from __future__ import annotations
import asyncio
import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type
from datetime import datetime

logger = logging.getLogger("omniagent")


class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    THINKING = "thinking"
    WAITING = "waiting"
    ERROR = "error"
    DONE = "done"


@dataclass
class AgentConfig:
    """智能体配置 - 每个智能体可独立配置"""
    name: str
    role: str = "assistant"
    goal: str = "协助用户完成任务"
    backstory: str = ""
    model: str = "auto"
    temperature: float = 0.7
    max_iterations: int = 25
    max_tokens: int = 4096
    allow_delegation: bool = True
    allow_code_exec: bool = False
    verbose: bool = False
    memory_enabled: bool = True
    tools: List[str] = field(default_factory=list)
    sub_agents: List[str] = field(default_factory=list)


class Agent:
    """
    核心智能体类 - 融合多项目最佳设计:
    - AutoGPT: 自主任务分解与执行
    - CrewAI: 角色定义与协作
    - Hermes Agent: 自改进能力
    - Agno: 生产级API设计
    """

    def __init__(self, config: AgentConfig):
        self.config = config
        self.status = AgentStatus.IDLE
        self.memory: Dict[str, Any] = {}
        self.skills: Dict[str, Callable] = {}
        self.tool_results: List[Dict] = []
        self._task_history: List[Dict] = []
        self._start_time: Optional[datetime] = None

    async def think(self, task: str, context: Optional[Dict] = None) -> str:
        """思考与规划 - AutoGPT 式自主推理 + ReAct 模式"""
        self.status = AgentStatus.THINKING
        logger.info(f"[{self.config.name}] Thinking about: {task}")

        plan = await self._decompose_task(task)
        self._task_history.append({"task": task, "plan": plan, "timestamp": datetime.now().isoformat()})
        return plan

    async def act(self, plan: str) -> Dict[str, Any]:
        """执行计划 - 调用工具与子智能体"""
        self.status = AgentStatus.RUNNING
        results = {}
        for step in plan.split("\n"):
            step = step.strip()
            if not step:
                continue
            result = await self._execute_step(step)
            results[step] = result
        self.status = AgentStatus.DONE
        return results

    async def _decompose_task(self, task: str) -> str:
        """任务分解 - AutoGPT/Superpowers 的任务链模式"""
        return f"1. 分析任务: {task}\n2. 查找相关工具\n3. 执行子任务\n4. 汇总结果"

    async def _execute_step(self, step: str) -> Any:
        """执行单步 - 工具调用、子智能体委派"""
        for skill_name, skill_fn in self.skills.items():
            if skill_name in step.lower():
                return await skill_fn(step)
        return {"status": "skipped", "reason": f"no matching skill for: {step}"}

    def register_skill(self, name: str, fn: Callable):
        """注册技能 - skills 框架模式"""
        self.skills[name] = fn

    async def reflect(self) -> Dict[str, Any]:
        """自省改进 - Hermes Agent 自改进模式"""
        return {
            "tasks_completed": len(self._task_history),
            "tools_used": len(self.tool_results),
            "memory_size": len(self.memory),
            "suggestions": []
        }

    def save_state(self) -> Dict:
        return {
            "config": {
                "name": self.config.name,
                "role": self.config.role,
                "goal": self.config.goal
            },
            "task_history": self._task_history[-50:],
            "memory_keys": list(self.memory.keys())
        }
