"""Web接口 - 融合 Vercel AI SDK 和 Mastra Studio 的Web界面"""
from __future__ import annotations
import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("omniagent.web")


class AgentWebUI:
    """
    Web UI 接口 - 融合:
    - Vercel AI SDK: useChat hooks, streaming
    - Mastra Studio: 智能体管理工作台
    - LangSmith: 可观测性仪表板
    - AutoGen Studio: 无代码 GUI
    """

    def __init__(self, agent_system: Any):
        self.agent_system = agent_system
        self._sessions: Dict[str, Dict] = {}

    def create_session(self, session_id: str):
        self._sessions[session_id] = {"messages": [], "context": {}}

    async def handle_message(self, session_id: str, message: str) -> Dict:
        session = self._sessions.get(session_id)
        if not session:
            self.create_session(session_id)
            session = self._sessions[session_id]
        session["messages"].append({"role": "user", "content": message})

        response = await self.agent_system.process(message, session["context"])
        session["messages"].append({"role": "assistant", "content": response})
        return {"response": response, "session_id": session_id}

    def get_session_history(self, session_id: str, limit: int = 50) -> list:
        session = self._sessions.get(session_id)
        return session["messages"][-limit:] if session else []

    def to_openai_spec(self) -> Dict:
        """生成 OpenAI-compatible API 规范"""
        return {
            "id": "omniagent",
            "object": "model",
            "created": 1710000000,
            "owned_by": "omniagent"
        }
