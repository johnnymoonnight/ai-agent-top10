"""智能体编排器 - 融合 CrewAI/AutoGen/MetaGPT 的多智能体协作"""
from __future__ import annotations
import asyncio
import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime

logger = logging.getLogger("omniagent.orchestrator")


class ProcessType(Enum):
    SEQUENTIAL = "sequential"
    HIERARCHICAL = "hierarchical"
    CONSENSUS = "consensus"
    DEBATE = "debate"
    SWARM = "swarm"


class Orchestrator:
    """
    多智能体编排器 - 融合:
    - CrewAI: 角色协作 + Flows
    - AutoGen: 对话式多智能体
    - MetaGPT: SOP驱动流程
    - TradingAgents: 辩论式决策
    """

    def __init__(self, name: str = "orchestrator"):
        self.name = name
        self.agents: Dict[str, Any] = {}
        self.workflows: Dict[str, Dict] = {}
        self._history: List[Dict] = []

    def register_agent(self, agent: Any, agent_id: Optional[str] = None):
        aid = agent_id or agent.config.name
        self.agents[aid] = agent
        logger.info(f"Registered agent: {aid}")

    async def run_sequential(self, agents: List[str], task: str) -> List[Any]:
        """顺序执行 - CrewAI sequential process"""
        results = []
        for aid in agents:
            agent = self.agents.get(aid)
            if not agent:
                continue
            plan = await agent.think(task, context={"prev_results": results})
            result = await agent.act(plan)
            results.append({aid: result})
            self._history.append({
                "agent": aid, "task": task, "result": result,
                "timestamp": datetime.now().isoformat()
            })
        return results

    async def run_debate(self, agents: List[str], topic: str, rounds: int = 3) -> Dict:
        """辩论模式 - TradingAgents 多智能体辩论决策"""
        opinions = {}
        for r in range(rounds):
            round_opinions = {}
            for aid in agents:
                agent = self.agents.get(aid)
                if not agent:
                    continue
                context = {"round": r + 1, "other_opinions": opinions}
                plan = await agent.think(f"Round {r+1} debate on: {topic}", context)
                round_opinions[aid] = plan
            opinions[r] = round_opinions
        return self._synthesize_debate(opinions)

    async def run_hierarchical(self, manager: str, workers: List[str], task: str) -> Dict:
        """层级管理 - MetaGPT/CrewAI hierarchical 模式"""
        mgr = self.agents.get(manager)
        if not mgr:
            return {"error": f"Manager {manager} not found"}
        plan = await mgr.think(f"作为管理者，分配任务给以下成员: {workers}. 任务: {task}")
        worker_results = {}
        for wid in workers:
            worker = self.agents.get(wid)
            if not worker:
                continue
            subtask = plan
            wplan = await worker.think(subtask)
            worker_results[wid] = await worker.act(wplan)
        return {"plan": plan, "results": worker_results}

    def _synthesize_debate(self, opinions: Dict) -> Dict:
        final = {}
        for rnd, ops in opinions.items():
            final[f"round_{rnd}"] = ops
        final["consensus"] = "synthesized from multi-agent debate"
        return final

    def get_history(self, limit: int = 10) -> List[Dict]:
        return self._history[-limit:]


AgentOrchestrator = Orchestrator
