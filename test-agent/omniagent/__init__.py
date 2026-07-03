"""OmniAgent - 融合 Top 10 AI智能体框架的超级Agent"""
from __future__ import annotations

__version__ = "0.2.0"

from .core.base import BaseAgent
from .core.orchestrator import AgentOrchestrator
from .core.skill import SkillRegistry, SkillBase
from .core.message import MessageBus, Message
from .tools import ToolRegistry, CodeExecutor, WebSearch, FileSystem
from .memory import MemoryStore, MemoryItem
from .workflow import WorkflowEngine, WorkflowDefinition
from .rag import RAGPipeline, VectorStore
from .mcp import MCPServerManager, MCPServer, MCPTool
from .observability import Tracer, Evaluator
from .plugins import PluginManager, PluginBase
from .web import AgentWebUI

__all__ = [
    "BaseAgent", "AgentOrchestrator", "SkillRegistry", "SkillBase",
    "MessageBus", "Message",
    "ToolRegistry", "CodeExecutor", "WebSearch", "FileSystem",
    "MemoryStore", "MemoryItem",
    "WorkflowEngine", "WorkflowDefinition",
    "RAGPipeline", "VectorStore",
    "MCPServerManager", "MCPServer", "MCPTool",
    "Tracer", "Evaluator",
    "PluginManager", "PluginBase",
    "AgentWebUI",
]
