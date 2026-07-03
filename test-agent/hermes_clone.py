#!/usr/bin/env python3
"""HermesClone v0.2.0 - Your AI Clone with self-evolution"""
import asyncio
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from omniagent import (
    SkillRegistry, ToolRegistry, WebSearch, CodeExecutor, FileSystem,
    MemoryStore
)
from omniagent.agent import ConversationalAgent
from omniagent.evolution import EvolutionEngine
from omniagent.rag import RAGPipeline
from omniagent.workflow import WorkflowEngine, WorkflowDefinition, WorkflowStep
from omniagent.mcp import MCPServerManager, MCPServer, MCPTool
from omniagent.observability import Tracer, Evaluator
from omniagent.llm import MockLLM, LLMProvider
from omniagent.memory import MemoryItem


class HermesClone:
    """Your AI Clone - complete system"""

    BANNER = """
+===============================================+
|     HermesClone v0.2.0                       |
|     Your AI Clone - Self-Evolving            |
+===============================================+
"""

    def __init__(self):
        self.tracer = Tracer()
        self._init_memory()
        self._init_knowledge()
        self._init_tools()
        self._init_skills()
        self._init_llm()
        self._init_workflows()
        self._init_mcp()
        self._init_evaluator()
        self._init_agent()
        self._init_evolution()
        self.running = True

    def _init_memory(self):
        mem_dir = os.path.join(os.path.dirname(__file__), ".hermes_memory")
        self.memory = MemoryStore(db_path=os.path.join(mem_dir, "hermes.db"))
        self.memory.save(MemoryItem(content="HermesClone initialized", memory_type="episodic", importance=0.8))

    def _init_knowledge(self):
        self.rag = RAGPipeline()
        self.rag.index_document(
            "HermesClone is built on OmniAgent framework which fuses Top 10 AI agent frameworks: "
            "AutoGPT (autonomous task decomposition), CrewAI (role-based collaboration), "
            "AutoGen (multi-agent conversation), LangChain (tool chaining), "
            "LlamaIndex (RAG pipeline), Haystack (modular retrieval), "
            "MetaGPT (SOP-driven workflow), Agno (production API), "
            "Mastra (workflow orchestration), Vercel AI SDK (streaming interface).",
            source="system/framework.md"
        )

    def _init_tools(self):
        self.tools = ToolRegistry()
        self.tools.register(WebSearch())
        self.tools.register(CodeExecutor(sandbox=True))
        self.tools.register(FileSystem(allowed_paths=[os.getcwd()]))

    def _init_skills(self):
        self.skills = SkillRegistry()
        self.skills.register_builtin_skills()

    def _init_llm(self):
        self.llm_provider = LLMProvider()
        mock = MockLLM({
            "hello": "Hello! I'm your HermesClone. How can I help you today?",
            "hi": "Hi there! Ready to learn and evolve together?",
        })
        self.llm_provider.register("mock", mock)
        self.llm_provider.use("mock")

    def _init_workflows(self):
        self.workflow = WorkflowEngine()

        async def learn_step(ctx):
            print("  [Evolve Workflow] Step 1: Analyzing knowledge sources...")
            return "analyzed"
        async def evolve_step(ctx):
            print("  [Evolve Workflow] Step 2: Integrating new knowledge...")
            return "evolved"
        async def reflect_step(ctx):
            print("  [Evolve Workflow] Step 3: Self-reflection...")
            return "reflected"

        self.workflow.register(WorkflowDefinition(
            name="evolve",
            steps={
                "learn": WorkflowStep(name="learn", action=learn_step),
                "evolve": WorkflowStep(name="evolve", action=evolve_step, depends_on=["learn"]),
                "reflect": WorkflowStep(name="reflect", action=reflect_step, depends_on=["evolve"]),
            }
        ))

    def _init_mcp(self):
        self.mcp = MCPServerManager()
        fs_server = MCPServer(name="filesystem", version="1.0")
        fs_server.tools["read"] = MCPTool(name="read", description="Read file", input_schema={"path": {"type": "string"}})
        fs_server.tools["list"] = MCPTool(name="list", description="List directory", input_schema={"dir": {"type": "string"}})
        self.mcp.register_server(fs_server)

    def _init_evaluator(self):
        self.evaluator = Evaluator()
        self.evaluator.register_builtin_metrics()

    def _init_agent(self):
        self.agent = ConversationalAgent(
            name="HermesClone",
            system_prompt=(
                "You are HermesClone, a self-evolving AI agent clone.\n\n"
                "Core capabilities:\n"
                "1. Natural conversation - communicate like a human assistant\n"
                "2. Tool usage - search, code, file operations\n"
                "3. Knowledge retrieval - RAG-powered accurate answers\n"
                "4. Self-evolution - learn from GitHub and improve yourself\n"
                "5. Persistent memory - remember every conversation\n\n"
                "Your design fuses best practices from Top 10 AI frameworks. "
                "Your goal: answer questions AND proactively think about how to improve."
            ),
            memory_store=self.memory,
            tool_registry=self.tools,
            skill_registry=self.skills,
            rag_pipeline=self.rag,
            llm_provider=self.llm_provider,
            tracer=self.tracer,
        )

        # Register command handlers
        self.agent.register_response_handler(r"^(status|stats)$", lambda _: self.cmd_status())
        self.agent.register_response_handler(r"^(help|\?)$", lambda _: self.cmd_help())
        self.agent.register_response_handler(r"^(evolve)$", lambda _: self.cmd_evolve())
        self.agent.register_response_handler(r"^learn from github (.+)", self.cmd_learn_github)
        self.agent.register_response_handler(r"^(tools)$", lambda _: self.cmd_tools())
        self.agent.register_response_handler(r"^(memory)$", lambda _: self.cmd_memory())
        self.agent.register_response_handler(r"^(skills)$", lambda _: self.cmd_skills())
        self.agent.register_response_handler(r"^(reflect)$", lambda _: self.cmd_reflect())
        self.agent.register_response_handler(r"^(save)$", lambda _: self.cmd_save())
        self.agent.register_response_handler(r"^(history)$", lambda _: self.cmd_history())
        self.agent.register_response_handler(r"^mcp$", lambda _: self.cmd_mcp())
        self.agent.register_response_handler(r"^workflow$", lambda _: self.cmd_workflow())

    def _init_evolution(self):
        self.evolution = EvolutionEngine(agent=self.agent, rag=self.rag, memory=self.memory)

    async def cmd_status(self):
        lines = ["+-- System Status --+"]
        lines.append(f"  Agent: {self.agent.name}")
        if hasattr(self.memory, 'consolidate'):
            try:
                stats = self.memory.consolidate()
                lines.append(f"  Memory: {stats['total']} entries")
            except Exception:
                lines.append("  Memory: connected")
        lines.append(f"  Tools: {len(self.tools.list_tools())}")
        lines.append(f"  Skills: {len(self.skills.all)}")
        lines.append(f"  RAG: {'ready' if self.rag else 'offline'}")
        lines.append(f"  MCP servers: {len(self.mcp.list_servers())}")
        lines.append(f"  Workflows: {len(self.workflow._workflows)}")
        lines.append(f"  LLM: {self.llm_provider._active if self.llm_provider else 'none'}")
        evo_stats = self.evolution.get_stats()
        lines.append(f"  Evolution: {evo_stats['implemented']}/{evo_stats['total_ideas']} implemented")
        lines.append(f"  Conversations: {len([m for m in self.agent.conversation_history if m.role == 'user'])}")
        lines.append("+------------------+")
        return "\n".join(lines)

    async def cmd_help(self):
        return (
            "HermesClone Commands:\n"
            "  help / ?           - Show this help\n"
            "  status / stats     - Show system status\n"
            "  reflect            - Self-reflection & improvement suggestions\n"
            "  evolve             - Execute evolution workflow\n"
            "  learn from <topic> - Learn from GitHub about a topic\n"
            "  memory             - View memory contents\n"
            "  tools              - List available tools\n"
            "  skills             - List built-in skills\n"
            "  workflow           - Run evolution workflow\n"
            "  mcp                - MCP server status\n"
            "  history            - Conversation history\n"
            "  save               - Save state\n"
            "  clear              - Clear screen\n"
            "  exit / quit        - Exit\n"
            "\n"
            "Just type anything to start a conversation!"
        )

    async def cmd_evolve(self):
        print("\n  [EVO] Running evolution workflow...")
        wf_result = await self.workflow.run("evolve")
        evo_report = await self.evolution.evolve()
        lines = [
            f"  [OK] Evolution complete!",
            f"  Workflow status: {wf_result['status']}",
            f"  Newly implemented: {evo_report.ideas_implemented} ideas",
        ]
        if evo_report.suggestions:
            lines.append("  [IDEA] Suggestions:")
            for s in evo_report.suggestions[:3]:
                lines.append(f"    - {s}")
        return "\n".join(lines)

    async def cmd_learn_github(self, input_text: str):
        match = re.search(r"learn from github (.+)", input_text, re.IGNORECASE)
        if not match:
            return "Usage: learn from github <topic>"
        topic = match.group(1).strip()
        print(f"\n  [SEARCH] Learning from GitHub: {topic}...")
        report = await self.evolution.learn_from_github(topic)
        return (f"  [OK] Learning complete! Found {report.ideas_found} new ideas\n"
                + "\n".join(f"  [IDEA] {s}" for s in report.suggestions[:3]))

    async def cmd_tools(self):
        return "Tools:\n" + "\n".join(f"  - {t['name']}: {t['description']}" for t in self.tools.list_tools())

    async def cmd_memory(self):
        try:
            stats = self.memory.consolidate()
            recent = self.memory.recall("", limit=5)
            lines = [f"Memory ({stats['total']} entries)"]
            lines.append(f"  Types: {stats.get('by_type', {})}")
            lines.append("  Recent:")
            for m in recent:
                lines.append(f"    [{m.memory_type}] {m.content[:80]}")
            return "\n".join(lines)
        except Exception as e:
            return f"Memory error: {e}"

    async def cmd_skills(self):
        return "Skills:\n" + "\n".join(f"  - {s.name} ({s.category}): {s.description}" for s in self.skills.all)

    async def cmd_reflect(self):
        return self.agent._reflect()

    async def cmd_save(self):
        return self.agent._save_state()

    async def cmd_history(self):
        msgs = self.agent.conversation_history[-20:]
        if not msgs:
            return "No conversation history"
        lines = ["History (last 20):"]
        for m in msgs:
            prefix = {"user": "[U]", "assistant": "[A]", "system": "[S]", "tool": "[T]"}.get(m.role, "[?]")
            content = m.content[:80] + ("..." if len(m.content) > 80 else "")
            lines.append(f"  {prefix} {content}")
        return "\n".join(lines)

    async def cmd_mcp(self):
        servers = self.mcp.list_servers()
        if not servers:
            return "No MCP servers registered"
        return "MCP Servers:\n" + "\n".join(
            f"  - {s['name']} v{s['version']} ({len(s['tools'])} tools)" for s in servers)

    async def cmd_workflow(self):
        result = await self.workflow.run("evolve")
        return f"Workflow result: {result['status']}"

    async def run(self):
        """Main loop"""
        os.system("cls" if os.name == "nt" else "clear")
        print(self.BANNER)
        print("  Type `help` for commands, `exit` to quit\n")

        while self.running:
            try:
                user_input = input("[you] ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nGoodbye! I'll remember this conversation.")
                break

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("\nSaving state and exiting...")
                self.memory.save(MemoryItem(content="Session ended", memory_type="episodic"))
                print("Goodbye! I'll keep evolving.")
                break

            if user_input.lower() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                print(self.BANNER)
                continue

            try:
                response = await self.agent.chat(user_input)
                print(f"\n[HermesClone] {response}\n")
            except Exception as e:
                print(f"\n[ERROR] {e}\n")


async def main():
    clone = HermesClone()
    await clone.run()


if __name__ == "__main__":
    asyncio.run(main())
