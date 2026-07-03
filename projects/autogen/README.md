# AutoGen (Microsoft)

**Stars**: 59,400+ | **语言**: Python / C# / TypeScript | **许可证**: CC-BY-4.0 / MIT

## 基本信息

- **仓库**: [microsoft/autogen](https://github.com/microsoft/autogen)
- **官网**: [https://microsoft.github.io/autogen/](https://microsoft.github.io/autogen/)
- **Forks**: 8,900+
- **状态**: 维护模式（推荐使用 Microsoft Agent Framework）

## 简介

AutoGen 是微软研究院推出的多智能体对话系统框架。支持构建可定制的多智能体应用，智能体可以自主行动或与人类协作。虽然目前已进入维护模式（由社区管理），但其架构设计对整个智能体生态产生了深远影响。微软推出了 Microsoft Agent Framework (MAF) 1.0 作为其企业级继任者。

## 架构设计

- **Core API**: 消息传递、事件驱动智能体、分布式运行时
- **AgentChat API**: 快速原型开发的高层 API
- **Extensions API**: 第一/三方扩展
- **AutoGen Studio**: 无代码 GUI 构建多智能体应用
- **AutoGen Bench**: 智能体性能基准测试

## 快速开始

```python
# 安装
pip install -U "autogen-agentchat" "autogen-ext[openai]"

# 使用
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    model_client = OpenAIChatCompletionClient(model="gpt-4.1")
    agent = AssistantAgent("assistant", model_client=model_client)
    print(await agent.run(task="Say 'Hello World!'"))
    await model_client.close()

asyncio.run(main())
```

## 使用场景

- 多智能体对话系统
- 人机协作工作流
- 智能体研究与教育
- 微软生态集成

## 注意事项

- AutoGen 已进入维护模式，推荐新项目使用 Microsoft Agent Framework
- 社区仍可贡献 bug 修复和安全补丁
- 现有用户可以继续使用但不会获得新功能
