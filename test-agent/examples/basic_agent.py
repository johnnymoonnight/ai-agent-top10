"""基础单智能体示例"""
import asyncio
from omniagent import BaseAgent, AgentConfig, SkillRegistry, Skill, ToolRegistry, WebSearch

async def main():
    registry = SkillRegistry()
    registry.register(Skill(name="greet", description="Say hello"))

    tools = ToolRegistry()
    tools.register(WebSearch())

    agent = BaseAgent(AgentConfig(name="OmniAgent", goal="assist user"))
    plan = await agent.think("test")
    print(f"Plan: {plan}")
    result = await agent.act("greet\nanalyze")
    print(f"Result: {result}")
    state = agent.save_state()
    print(f"State: {len(state['task_history'])} tasks")

asyncio.run(main())
