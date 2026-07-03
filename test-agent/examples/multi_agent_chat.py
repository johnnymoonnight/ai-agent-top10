"""多智能体协作示例 - 辩论模式"""
import asyncio
from omniagent import BaseAgent, MessageBus, Message, AgentOrchestrator

async def main():
    bus = MessageBus()
    orchestrator = AgentOrchestrator()

    # 创建两个智能体
    alice = BaseAgent(name="Alice")
    bob = BaseAgent(name="Bob")

    orchestrator.register_agent(alice)
    orchestrator.register_agent(bob)

    # 订阅消息
    alice_results = []
    async def alice_handler(msg: Message):
        alice_results.append(f"Alice received: {msg.content}")

    bob_results = []
    async def bob_handler(msg: Message):
        bob_results.append(f"Bob received: {msg.content}")

    bus.subscribe("text", alice_handler)
    bus.subscribe("text", bob_handler)

    # 发送消息
    await bus.publish(Message(
        source="user", target="all",
        content="What's the best AI framework?",
        msg_type="text"
    ))

    print(alice_results)
    print(bob_results)

asyncio.run(main())
