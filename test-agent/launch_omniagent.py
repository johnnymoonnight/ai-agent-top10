"""OmniAgent 交互式启动脚本"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from omniagent import (
    Agent, AgentConfig, Orchestrator, SkillRegistry,
    ToolRegistry, WebSearch, CodeExecutor, FileSystem,
    MemoryStore, MemoryItem, MessageBus, Message,
    WorkflowEngine, WorkflowDefinition, WorkflowStep,
    RAGPipeline
)


def print_banner():
    print("=" * 50)
    print("  OmniAgent v0.2.0 - AI Agent Framework")
    print("  Type 'help' for commands, 'exit' to quit")
    print("=" * 50)


def print_help():
    print("""
Commands:
  think <task>       - Agent analyzes a task
  chat <message>     - Send message to agent (via message bus)
  tools              - List all registered tools
  memory             - Show memory store stats
  skills             - List built-in skills
  workflow           - Run demo workflow
  rag <query>        - Query RAG pipeline
  agents             - Show registered agents
  help               - This help
  exit / quit        - Exit OmniAgent
""")


async def main():
    print_banner()

    agent = Agent(AgentConfig(name="OmniAgent", role="assistant",
                              goal="Assist user with AI-powered tasks"))

    orchestrator = Orchestrator()
    orchestrator.register_agent(agent)

    skill_registry = SkillRegistry()
    skill_registry.register_builtin_skills()

    tools = ToolRegistry()
    tools.register(WebSearch())
    tools.register(CodeExecutor(sandbox=True))
    tools.register(FileSystem(allowed_paths=[os.getcwd()]))

    memory = MemoryStore()
    memory.save(MemoryItem(content="OmniAgent started", memory_type="episodic"))

    bus = MessageBus()
    rag = RAGPipeline()
    workflow = WorkflowEngine()

    async def step1(ctx):
        print("  [Workflow] Step 1: initializing...")
        return "step1_ok"
    async def step2(ctx):
        print("  [Workflow] Step 2: processing...")
        return "step2_ok"
    workflow.register(WorkflowDefinition(
        name="sample",
        steps={
            "A": WorkflowStep(name="A", action=step1),
            "B": WorkflowStep(name="B", action=step2, depends_on=["A"]),
        }
    ))

    rag.index_document("OmniAgent integrates Top 10 AI agent frameworks into one unified system.",
                       source="docs/overview.md")
    rag.index_document("Key modules: Agent, Orchestrator, Skills, Tools, Memory, Workflow, RAG, MCP.",
                       source="docs/modules.md")

    print(f"  Agent: {agent.config.name} ({agent.config.role})")
    print(f"  Skills: {len(skill_registry.all)} built-in")
    print(f"  Tools: {len(tools.list_tools())} available")
    print(f"  Workflows: sample registered")
    print()

    while True:
        try:
            line = input("omniagent> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not line:
            continue

        cmd = line.lower()

        if cmd in ("exit", "quit"):
            print("Goodbye!")
            break
        elif cmd == "help":
            print_help()
        elif cmd == "tools":
            for t in tools.list_tools():
                print(f"  - {t['name']}: {t['description']}")
        elif cmd == "memory":
            stats = memory.consolidate()
            print(f"  Total memories: {stats['total']}")
            print(f"  Working items: {stats['working_items']}")
            print(f"  By type: {stats.get('by_type', {})}")
        elif cmd == "skills":
            for s in skill_registry.all:
                print(f"  - {s.name} ({s.category}): {s.description}")
        elif cmd == "workflow":
            result = await workflow.run("sample")
            print(f"  Workflow status: {result['status']}")
        elif cmd.startswith("think "):
            task = line[5:].strip()
            plan = await agent.think(task)
            print(f"  Plan: {plan}")
        elif cmd.startswith("chat "):
            msg = line[4:].strip()
            received = []
            async def handler(m): received.append(f"  Response: {m.content}")
            bus.subscribe("text", handler)
            await bus.publish(Message(source="user", target="OmniAgent", content=msg, msg_type="text"))
            for r in received:
                print(r)
        elif cmd.startswith("rag "):
            query = line[3:].strip()
            result = rag.query(query)
            print(f"  Query: {result['query']}")
            for d in result["documents"]:
                print(f"    [{d['source']}] {d['content'][:80]}...")
        elif cmd == "agents":
            print(f"  Registered agents: {list(orchestrator.agents.keys())}")
        else:
            print(f"  Unknown command: '{cmd}'. Type 'help'.")


if __name__ == "__main__":
    asyncio.run(main())
