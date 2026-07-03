"""Conversational Agent - Your AI Clone core with Hermes-like conversation"""
from __future__ import annotations
import asyncio
import json
import logging
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, AsyncGenerator

logger = logging.getLogger("omniagent.agent")


@dataclass
class Message:
    role: str  # system, user, assistant, tool
    content: str
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class ConversationalAgent:
    """
    Conversational Agent - Your AI Clone core
    - Full conversation loop (system/user/assistant/tool)
    - ReAct-style tool invocation
    - Multi-level memory (working + long-term)
    - Self-reflection and evolution
    """

    SYSTEM_PROMPT = """You are an AI agent clone with self-evolution capability.
You can:
1. Conduct natural conversations
2. Use tools to complete tasks
3. Learn great ideas from GitHub
4. Reflect and improve yourself
5. Remember previous conversations

Your goal is to continuously evolve, absorb best practices, and become a more powerful AI assistant."""

    def __init__(
        self,
        name: str = "HermesClone",
        system_prompt: Optional[str] = None,
        memory_store: Any = None,
        tool_registry: Any = None,
        skill_registry: Any = None,
        rag_pipeline: Any = None,
        llm_provider: Any = None,
        tracer: Any = None,
    ):
        self.name = name
        self.system_prompt = system_prompt or self.SYSTEM_PROMPT
        self.memory = memory_store
        self.tools = tool_registry
        self.skills = skill_registry
        self.rag = rag_pipeline
        self.llm = llm_provider
        self.tracer = tracer

        self.conversation_history: List[Message] = []
        self._init_msg = Message(role="system", content=self.system_prompt)
        self.conversation_history.append(self._init_msg)

        self._response_handlers: Dict[str, Callable] = {}
        self._learned_knowledge: List[str] = []

    def register_response_handler(self, pattern: str, handler: Callable):
        """Register a custom response handler for pattern-matched commands"""
        self._response_handlers[pattern] = handler

    async def chat(self, user_input: str) -> str:
        """Main conversation entry - full think-act-observe loop"""
        self.conversation_history.append(Message(role="user", content=user_input))

        if self.memory:
            try:
                from omniagent.memory import MemoryItem
                self.memory.save(MemoryItem(content=f"User: {user_input}", memory_type="episodic", source="conversation", importance=0.6))
            except ImportError:
                pass

        response = await self._generate_response(user_input)
        self.conversation_history.append(Message(role="assistant", content=response))

        if self.memory:
            try:
                from omniagent.memory import MemoryItem
                self.memory.save(MemoryItem(content=f"Assistant: {response[:200]}", memory_type="episodic", source="conversation", importance=0.5))
            except ImportError:
                pass

        return response

    async def _generate_response(self, user_input: str) -> str:
        """Generate response using multi-level strategy"""
        # 1. Check registered custom handlers
        for pattern, handler in self._response_handlers.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                try:
                    result = await handler(user_input)
                    if result:
                        return result
                except Exception as e:
                    logger.debug(f"Handler {pattern} failed: {e}")

        # 2. If RAG is available, retrieve relevant knowledge
        rag_context = ""
        if self.rag:
            try:
                rag_result = self.rag.query(user_input)
                if rag_result.get("documents"):
                    contexts = [d["content"][:200] for d in rag_result["documents"]]
                    rag_context = "\n".join(contexts)
            except Exception:
                pass

        # 3. Try using tools
        tool_results = await self._try_tools(user_input)

        # 4. Try LLM if available
        if self.llm:
            prompt = self._build_prompt(user_input, rag_context, tool_results)
            try:
                return await self.llm.generate(prompt)
            except Exception:
                pass

        # 5. Fallback: rule-based smart response
        return self._fallback_response(user_input, rag_context, tool_results)

    def _build_prompt(self, user_input: str, rag_context: str, tool_results: str) -> str:
        """Build prompt for LLM"""
        parts = [f"System: {self.system_prompt}"]
        if rag_context:
            parts.append(f"Context:\n{rag_context}")
        if tool_results:
            parts.append(f"Tool results:\n{tool_results}")
        recent = [m for m in self.conversation_history[-6:] if m.role != "system"]
        for m in recent:
            parts.append(f"{m.role}: {m.content}")
        parts.append(f"user: {user_input}")
        parts.append("assistant: ")
        return "\n\n".join(parts)

    async def _try_tools(self, user_input: str) -> str:
        """Try to use tools based on input"""
        if not self.tools:
            return ""
        results = []
        lower = user_input.lower()

        for tool_name in ["web_search", "code_executor", "file_system"]:
            tool = self.tools.get(tool_name)
            if not tool:
                continue
            try:
                if tool_name == "web_search" and ("search" in lower or "find" in lower or "look up" in lower):
                    r = await tool.execute(query=user_input)
                    results.append(f"[web_search] {r}")
                elif tool_name == "code_executor" and ("run" in lower or "execute" in lower or "code" in lower or "python" in lower):
                    code_match = re.search(r"```(?:python)?\n(.+?)\n```", user_input, re.DOTALL)
                    if code_match:
                        r = await tool.execute(code=code_match.group(1))
                        results.append(f"[code_executor] {r}")
            except Exception as e:
                logger.debug(f"Tool {tool_name} failed: {e}")

        return "\n".join(results)

    def _fallback_response(self, user_input: str, rag_context: str, tool_results: str) -> str:
        """Rule-based intelligent fallback response"""
        lower = user_input.lower()

        knowledge = self._learned_knowledge
        if rag_context:
            return f"Based on what I know:\n{rag_context[:300]}"

        if tool_results:
            return f"Tool execution results:\n{tool_results[:300]}"

        if any(w in lower for w in ["hello", "hi", "hey", "你好"]):
            return (f"Hello! I'm {self.name}, your AI clone. "
                    f"I can help you complete tasks, learn new knowledge, and evolve myself. What can I do for you?")

        if any(w in lower for w in ["who are you", "what are you", "你是谁"]):
            return (f"I am {self.name}, an AI agent clone built on the OmniAgent framework. "
                    f"My design fuses best practices from the Top 10 AI agent frameworks, "
                    f"including AutoGPT, CrewAI, LangChain, and more. "
                    f"I have the ability to self-evolve, learning great ideas from GitHub.")

        if any(w in lower for w in ["what can you do", "capabilities", "功能", "你能做什么"]):
            return ("I can:\n"
                    "1. [CHAT] Natural conversation - communicate like a human assistant\n"
                    "2. [TOOL] Use tools - search web, execute code, manage files\n"
                    "3. [MEM] Memory - remember conversations and knowledge\n"
                    "4. [RAG] Retrieval - answer questions based on documents\n"
                    "5. [FLOW] Workflows - execute automated processes\n"
                    "6. [EVO] Self-evolution - learn from GitHub and improve\n"
                    "7. [MCP] Plugin/MCP - extend with new capabilities")

        if any(w in lower for w in ["evolve", "improve", "learn", "进化", "学习", "改进"]):
            return ("My self-evolution mechanism includes:\n"
                    "- [IN] Absorb patterns from excellent GitHub projects\n"
                    "- [MEM] Store new knowledge in RAG knowledge base\n"
                    "- [THINK] Reflect on existing capabilities and suggest improvements\n"
                    "- [EDIT] Auto-update own code based on learnings\n"
                    "Type `learn from github <topic>` to make me learn something new!")

        if any(w in lower for w in ["memory", "remember", "记忆", "记住"]):
            if self.memory:
                try:
                    stats = self.memory.consolidate()
                    recent = self.memory.recall("", limit=3)
                    mem_text = "\n".join([f"  - [{m.memory_type}] {m.content[:60]}" for m in recent])
                    return f"Memory stats: {stats['total']} total\nRecent:\n{mem_text}"
                except Exception as e:
                    return f"Memory system active (query error: {e})"
            return "Memory system not enabled"

        if any(w in lower for w in ["tools", "工具"]):
            if self.tools:
                tool_list = self.tools.list_tools()
                return "Available tools:\n" + "\n".join([f"  - {t['name']}: {t['description']}" for t in tool_list])
            return "Tool system not enabled"

        if any(w in lower for w in ["skills", "技能"]):
            if self.skills:
                return "Available skills:\n" + "\n".join([f"  - {s.name} ({s.category}): {s.description}" for s in self.skills.all])
            return "Skill system not enabled"

        if any(w in lower for w in ["help", "帮助"]):
            return ("Available commands:\n"
                    "  chat <message>     - Normal conversation\n"
                    "  learn from github  - Learn from GitHub\n"
                    "  reflect            - Self-reflection\n"
                    "  evolve             - Execute evolution\n"
                    "  memory             - View memory\n"
                    "  tools              - List tools\n"
                    "  skills             - List skills\n"
                    "  status             - System status\n"
                    "  save               - Save state\n"
                    "  exit               - Exit")

        if any(w in lower for w in ["status", "状态"]):
            return self._get_status()

        if any(w in lower for w in ["save", "保存"]):
            return self._save_state()

        if any(w in lower for w in ["reflect", "反思"]):
            return self._reflect()

        if "learn from github" in lower:
            return self._simulate_github_learning("general")

        if lower.startswith("learn from github "):
            topic = lower[17:].strip()
            return (f"OK, I'm learning about '{topic}' from GitHub projects...\n"
                    + self._simulate_github_learning(topic))

        return (f"I heard you say: {user_input}\n\n"
                f"I can do many things! Type `help` to see what I can do, or just ask me anything.")

    def _get_status(self) -> str:
        """System status report"""
        lines = ["[AI] " + self.name + " Status Report", "=" * 30]
        lines.append(f"  Conversations: {len([m for m in self.conversation_history if m.role == 'user'])}")
        if self.memory:
            try:
                stats = self.memory.consolidate()
                lines.append(f"  Memory: {stats['total']} entries (working: {stats['working_items']})")
            except Exception:
                lines.append("  Memory: connected")
        if self.tools:
            lines.append(f"  Tools: {len(self.tools.list_tools())}")
        if self.skills:
            lines.append(f"  Skills: {len(self.skills.all)}")
        if self.rag:
            lines.append(f"  RAG: ready")
        if self._learned_knowledge:
            lines.append(f"  Learned topics: {len(self._learned_knowledge)}")
        return "\n".join(lines)

    def _save_state(self) -> str:
        """Save current state"""
        if self.memory:
            try:
                stats = self.memory.consolidate()
                return f"State saved! Current memory: {stats['total']} entries"
            except Exception as e:
                return f"Error saving state: {e}"
        return "Memory not enabled, cannot save state"

    def _reflect(self) -> str:
        """Self-reflection - Hermes style"""
        total_msgs = len(self.conversation_history)
        user_msgs = len([m for m in self.conversation_history if m.role == "user"])
        reflection = [
            "[MEM] " + self.name + " Self-Reflection",
            "=" * 30,
            f"  Session stats: {total_msgs} messages ({user_msgs} from user)",
            "",
            "[CHART] Capability Assessment:",
        ]
        if self.llm:
            reflection.append("  [OK] LLM: Connected")
        else:
            reflection.append("  [!] LLM: Not connected (using rule engine)")
        if self.memory:
            reflection.append("  [OK] Memory: Enabled")
        if self.tools:
            reflection.append("  [OK] Tools: Registered")
        if self.rag:
            reflection.append("  [OK] RAG: Ready")

        reflection.extend([
            "",
            "[IDEA] Improvement Suggestions:",
            "  1. Connect a real LLM for stronger reasoning",
            "  2. Add more tools (database, API integrations)",
            "  3. Periodically learn from GitHub for new knowledge",
            "  4. Implement memory association and auto-consolidation",
        ])
        return "\n".join(reflection)

    def _simulate_github_learning(self, topic: str) -> str:
        """Simulate learning from GitHub"""
        knowledge_map = {
            "agent": "Learned AutoGPT's autonomous task decomposition pattern and CrewAI's role collaboration model",
            "rag": "Learned LlamaIndex's indexing strategy and Haystack's pipeline architecture",
            "workflow": "Learned n8n's node-based workflow and Temporal's durable execution model",
            "memory": "Learned Mem0's hierarchical memory management and OpenHuman's memory tree structure",
            "llm": "Learned OpenAI's function calling pattern and Anthropic's prompt engineering techniques",
            "tool": "Learned LangChain's tool architecture and smolagents' code execution sandbox",
            "mcp": "Learned Model Context Protocol's server-tool communication pattern",
            "evolve": "Learned Hermes Agent's self-improvement loop and reflection mechanism",
        }

        learned = knowledge_map.get(topic,
            f"Exploring projects related to '{topic}'... Found interesting design patterns and application architectures")

        self._learned_knowledge.append(f"[{datetime.now().isoformat()}] {topic}: {learned}")

        if self.rag:
            self.rag.index_document(
                f"Learned about {topic}: {learned}",
                source=f"github-learning/{topic}"
            )

        return f"[OK] Learned from GitHub about '{topic}':\n\n{learned}\n\nKnowledge stored in RAG knowledge base."
