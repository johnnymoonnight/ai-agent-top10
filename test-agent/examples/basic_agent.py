"""基础单智能体示例"""
import asyncio
from omniagent import BaseAgent, SkillRegistry, SkillBase, ToolRegistry

class GreetSkill(SkillBase):
    def __init__(self):
        super().__init__("greet", "Say hello")

    async def execute(self, params: dict) -> str:
        return f"Hello, {params.get('name', 'world')}!"

async def main():
    registry = SkillRegistry()
    registry.register(GreetSkill())

    tools = ToolRegistry()
    tools.register(GreetSkill())

    agent = BaseAgent(name="OmniAgent", skill_registry=registry, tool_registry=tools)
    result = await agent.execute({"task": "greet", "name": "OmniAgent"})
    print(result)

asyncio.run(main())
