"""OmniAgent 全套测试"""
from __future__ import annotations
import pytest
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from omniagent.core.base import Agent, AgentConfig, BaseAgent
from omniagent.core.orchestrator import Orchestrator, AgentOrchestrator
from omniagent.core.skill import Skill, SkillRegistry, SkillBase
from omniagent.core.message import Message, MessageBus, MessagePriority
from omniagent.tools import ToolRegistry, CodeExecutor, WebSearch, FileSystem, BaseTool, ToolSpec
from omniagent.memory import MemoryStore, MemoryItem
from omniagent.workflow import WorkflowEngine, WorkflowDefinition, WorkflowStep
from omniagent.rag import RAGPipeline, Document, VectorStore
from omniagent.mcp import MCPServerManager, MCPServer, MCPTool
from omniagent.observability import Tracer, Evaluator, SpanStatus, EvalResult
from omniagent.plugins import PluginManager, PluginBase, PluginManifest
from omniagent.web import AgentWebUI
from omniagent.llm import MockLLM, EchoLLM, LLMProvider


# ===== core/base =====

class TestAgent:
    def test_create_agent(self):
        cfg = AgentConfig(name="test", role="coder", goal="write code")
        agent = Agent(cfg)
        assert agent.config.name == "test"
        assert agent.status.value == "idle"

    @pytest.mark.asyncio
    async def test_think(self):
        agent = Agent(AgentConfig(name="thinker"))
        plan = await agent.think("test task")
        assert "分析任务" in plan
        assert agent.status.value == "thinking"

    @pytest.mark.asyncio
    async def test_act(self):
        agent = Agent(AgentConfig(name="actor"))
        plan = "step1\nstep2"
        results = await agent.act(plan)
        assert len(results) == 2

    def test_register_skill(self):
        agent = Agent(AgentConfig(name="skilled"))
        async def dummy(p): return "done"
        agent.register_skill("test", dummy)
        assert "test" in agent.skills

    def test_save_state(self):
        agent = Agent(AgentConfig(name="stateful"))
        state = agent.save_state()
        assert state["config"]["name"] == "stateful"

    def test_baseagent_alias(self):
        assert BaseAgent is Agent


# ===== core/orchestrator =====

class TestOrchestrator:
    def test_register_agent(self):
        o = Orchestrator()
        agent = Agent(AgentConfig(name="alice"))
        o.register_agent(agent)
        assert "alice" in o.agents

    @pytest.mark.asyncio
    async def test_sequential(self):
        o = Orchestrator()
        a1 = Agent(AgentConfig(name="a1"))
        a2 = Agent(AgentConfig(name="a2"))
        o.register_agent(a1)
        o.register_agent(a2)
        results = await o.run_sequential(["a1", "a2"], "go")
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_debate(self):
        o = Orchestrator()
        a1 = Agent(AgentConfig(name="debater1"))
        a2 = Agent(AgentConfig(name="debater2"))
        o.register_agent(a1)
        o.register_agent(a2)
        result = await o.run_debate(["debater1", "debater2"], "topic", rounds=1)
        assert "round_0" in result

    def test_orchestrator_alias(self):
        assert AgentOrchestrator is Orchestrator


# ===== core/skill =====

class TestSkill:
    def test_register(self):
        r = SkillRegistry()
        s = Skill(name="test", description="test skill")
        r.register(s)
        assert r.get("test") is s

    def test_search(self):
        r = SkillRegistry()
        r.register(Skill(name="python", description="Python coding"))
        r.register(Skill(name="debug", description="Find bugs"))
        results = r.search("python")
        assert len(results) == 1

    def test_categories(self):
        r = SkillRegistry()
        r.register(Skill(name="a", description="first", category="dev"))
        r.register(Skill(name="b", description="second", category="dev"))
        assert "dev" in r.categories
        assert len(r.list_by_category("dev")) == 2

    def test_builtins(self):
        r = SkillRegistry()
        r.register_builtin_skills()
        assert len(r.all) == 12

    def test_skillbase_alias(self):
        assert issubclass(SkillBase, Skill)


# ===== core/message =====

class TestMessageBus:
    @pytest.mark.asyncio
    async def test_publish_subscribe(self):
        bus = MessageBus()
        received = []
        async def handler(msg): received.append(msg)
        bus.subscribe("text", handler)
        msg = Message(source="test", target="all", content="hello", msg_type="text")
        await bus.publish(msg)
        assert len(received) == 1
        assert received[0].content == "hello"

    @pytest.mark.asyncio
    async def test_consume(self):
        bus = MessageBus()
        msg = Message(source="a", target="b", content="data")
        await bus.publish(msg)
        consumed = await bus.consume(timeout=0.5)
        assert consumed is not None
        assert consumed.content == "data"

    def test_history(self):
        bus = MessageBus()
        async def go():
            for i in range(3):
                await bus.publish(Message(source="s", target="t", content=str(i)))
            assert len(bus.get_history()) == 3
        asyncio.run(go())

    def test_priority(self):
        assert MessagePriority.HIGH.value == 2


# ===== tools =====

class TestTools:
    def test_tool_spec(self):
        spec = ToolSpec(name="calc", description="calculator")
        assert spec.name == "calc"

    def test_tool_registry(self):
        reg = ToolRegistry()
        tool = WebSearch()
        reg.register(tool)
        assert reg.get("web_search") is tool
        assert len(reg.list_tools()) == 1

    @pytest.mark.asyncio
    async def test_code_executor(self):
        exec = CodeExecutor()
        result = await exec.execute(code="print(42)")
        assert "42" in result.get("stdout", "")

    @pytest.mark.asyncio
    async def test_web_search(self):
        ws = WebSearch()
        result = await ws.execute(query="test")
        assert result["status"] == "ok"

    @pytest.mark.asyncio
    async def test_file_system_denied(self):
        fs = FileSystem(allowed_paths=["/safe"])
        result = await fs.execute(action="read", path="/etc/passwd")
        assert "not allowed" in result.get("error", "")

    def test_base_tool_abstract(self):
        with pytest.raises(TypeError):
            BaseTool(ToolSpec(name="x", description="x"))


# ===== memory =====

class TestMemory:
    def test_save_and_recall(self):
        m = MemoryStore(db_path=":memory:")
        m.save(MemoryItem(content="hello world", memory_type="semantic"))
        results = m.recall("hello")
        assert len(results) == 1
        assert results[0].content == "hello world"

    def test_working_memory(self):
        m = MemoryStore(db_path=":memory:")
        m.update_working("key", "value")
        assert m.get_working("key") == "value"
        m.clear_working()
        assert m.get_working("key") is None

    def test_consolidate(self):
        m = MemoryStore(db_path=":memory:")
        m.save(MemoryItem(content="a", memory_type="episodic"))
        m.save(MemoryItem(content="b", memory_type="semantic"))
        stats = m.consolidate()
        assert stats["total"] == 2

    def test_forget(self):
        m = MemoryStore(db_path=":memory:")
        m.save(MemoryItem(content="old", memory_type="episodic"))
        m.forget(memory_type="episodic")
        assert len(m.recall("old")) == 0


# ===== workflow =====

class TestWorkflow:
    @pytest.mark.asyncio
    async def test_simple_workflow(self):
        engine = WorkflowEngine()
        results = []
        async def step_a(ctx): results.append("a"); return "a_done"
        async def step_b(ctx): results.append("b"); return "b_done"
        engine.register(WorkflowDefinition(
            name="test",
            steps={
                "A": WorkflowStep(name="A", action=step_a),
                "B": WorkflowStep(name="B", action=step_b),
            }
        ))
        result = await engine.run("test")
        assert result["status"] == "completed"
        assert results == ["a", "b"]

    def test_workflow_not_found(self):
        engine = WorkflowEngine()
        result = asyncio.run(engine.run("nonexistent"))
        assert "error" in result

    def test_list_runs(self):
        engine = WorkflowEngine()
        assert len(engine.list_runs()) == 0


# ===== rag =====

class TestRAG:
    def test_index_and_retrieve(self):
        rag = RAGPipeline()
        rag.index_document("OmniAgent is a meta-agent framework.")
        assert rag.stats()["documents"] == 1

    def test_query(self):
        rag = RAGPipeline()
        rag.index_document("test content", source="test.txt")
        result = rag.query("test")
        assert result["query"] == "test"

    def test_vector_store(self):
        vs = VectorStore()
        vs.add(Document(content="doc1"))
        docs = vs.search([0.1, 0.2, 0.3])
        assert len(docs) >= 1


# ===== mcp =====

class TestMCP:
    def test_register_server(self):
        mgr = MCPServerManager()
        server = MCPServer(name="filesystem")
        mgr.register_server(server)
        assert len(mgr.list_servers()) == 1

    def test_register_tool(self):
        mgr = MCPServerManager()
        server = MCPServer(name="fs")
        mgr.register_server(server)
        tool = MCPTool(name="read", description="read file", input_schema={})
        mgr.register_tool("fs", tool)
        assert "read" in mgr.servers["fs"].tools

    @pytest.mark.asyncio
    async def test_call_tool(self):
        mgr = MCPServerManager()
        server = MCPServer(name="test")
        async def handler(args): return {"result": "ok"}
        tool = MCPTool(name="ping", description="ping", input_schema={}, handler=handler)
        server.tools["ping"] = tool
        mgr.register_server(server)
        result = await mgr.call_tool("test", "ping", {})
        assert result["result"] == "ok"

    def test_list_tools(self):
        mgr = MCPServerManager()
        assert mgr.list_tools() == []


# ===== observability =====

class TestObservability:
    def test_tracer(self):
        t = Tracer()
        span = t.start_span("test_span")
        t.end_span()
        assert len(t.get_trace()) == 1

    def test_tracer_nested(self):
        t = Tracer()
        span1 = t.start_span("parent")
        span2 = t.start_span("child")
        assert span2.parent_id == span1.span_id
        t.end_span()
        t.end_span()
        assert len(t.get_trace()) == 2

    def test_evaluator(self):
        e = Evaluator()
        e.register_builtin_metrics()
        result = asyncio.run(e.evaluate("latency", duration_ms=100))
        assert result.passed
        assert result.score > 0

    def test_evaluator_unknown(self):
        e = Evaluator()
        result = asyncio.run(e.evaluate("unknown_metric"))
        assert not result.passed


# ===== plugins =====

class TestPlugins:
    @pytest.mark.asyncio
    async def test_load_plugin(self):
        mgr = PluginManager()
        manifest = PluginManifest(name="test", version="1.0", description="test")
        class TestPlugin(PluginBase): pass
        await mgr.load_plugin(manifest, TestPlugin)
        assert len(mgr.list_plugins()) == 1
        assert mgr.get_plugin("test") is not None

    @pytest.mark.asyncio
    async def test_unload(self):
        mgr = PluginManager()
        manifest = PluginManifest(name="p", version="1.0", description="")
        await mgr.load_plugin(manifest, type("P", (PluginBase,), {}))
        await mgr.unload_plugin("p")
        assert len(mgr.list_plugins()) == 0


# ===== web =====

class TestWeb:
    @pytest.mark.asyncio
    async def test_handle_message(self):
        class FakeAgent:
            async def process(self, msg, ctx):
                return f"processed: {msg}"
        ui = AgentWebUI(FakeAgent())
        result = await ui.handle_message("s1", "hello")
        assert "processed: hello" in result["response"]

    def test_session(self):
        ui = AgentWebUI(None)
        ui.create_session("s1")
        history = ui.get_session_history("s1")
        assert history == []


# ===== llm =====

class TestLLM:
    @pytest.mark.asyncio
    async def test_mock_llm(self):
        llm = MockLLM({"hello": "world"})
        result = await llm.generate("say hello")
        assert result == "world"

    @pytest.mark.asyncio
    async def test_echo_llm(self):
        llm = EchoLLM()
        result = await llm.generate("echo this")
        assert result == "echo this"

    @pytest.mark.asyncio
    async def test_provider(self):
        p = LLMProvider()
        p.register("mock", MockLLM({"test": "passed"}))
        result = await p.generate("test prompt")
        assert result == "passed"


# ===== integration =====

class TestIntegration:
    @pytest.mark.asyncio
    async def test_agent_with_skills(self):
        registry = SkillRegistry()
        registry.register(Skill(name="greet", description="Greeting"))
        agent = Agent(AgentConfig(name="integrated"))
        results = await agent.act("greet\nother")
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_orchestrator_with_memory(self):
        o = Orchestrator()
        mem = MemoryStore(db_path=":memory:")
        agent = Agent(AgentConfig(name="mem_agent"))
        o.register_agent(agent)
        mem.save(MemoryItem(content="context data", memory_type="semantic"))
        results = await o.run_sequential(["mem_agent"], "use context")
        assert len(results) == 1
