"""多智能体协作示例"""
import asyncio
from omniagent import BaseAgent, AgentConfig, MessageBus, Message, Orchestrator

async def main():
    bus = MessageBus()
    orchestrator = Orchestrator()

    alice = BaseAgent(AgentConfig(name="Alice"))
    bob = BaseAgent(AgentConfig(name="Bob"))
    orchestrator.register_agent(alice)
    orchestrator.register_agent(bob)

    received = []
    async def handler(msg):
        received.append(f"{msg.source} -> {msg.target}: {msg.content}")
    bus.subscribe("text", handler)

    await bus.publish(Message(source="user", target="all", content="What's the best AI framework?", msg_type="text"))
    print(received)

asyncio.run(main())
