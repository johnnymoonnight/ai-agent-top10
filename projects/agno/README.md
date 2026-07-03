# Agno

**Stars**: 41,000+ | **语言**: Python | **许可证**: Apache-2.0

## 基本信息

- **仓库**: [agno-agi/agno](https://github.com/agno-agi/agno)
- **官网**: [https://docs.agno.com](https://docs.agno.com)
- **最新版本**: v2.6.20 (2026-06-26)
- **Forks**: 5,600+
- **Used by**: 2,700+

## 简介

Agno（原名 phidata）是一个 SDK，用于构建、运行和管理智能体平台。它支持使用任何智能体框架构建智能体，将它们作为生产服务运行（含追踪、调度、RBAC），并通过统一控制面板进行管理。核心承诺：拥有你的智能体栈（Own your agent stack）。

## 核心功能

- **Production API**: 50+ 端点，SSE/WebSocket 支持
- **Storage**: 在自有数据库中存储会话、记忆、知识
- **100+ Integrations**: 预构建工具包
- **Context Providers**: 实时数据接入（Slack, Drive, MCP 等）
- **Human Approval**: 人工审批流程
- **RBAC**: JWT 角色权限控制
- **多通道**: Slack, Telegram, WhatsApp, Discord, AG-UI
- **Scheduling**: Cron 调度和后台任务
- **Observability**: OpenTelemetry 追踪

## 使用示例

```python
from agno.agent import Agent

agent = Agent(
    name="My Agent",
    tools=[...],
    context_providers=[...],
)
agent.run("完成这个任务")
```

## 使用场景

- 企业级智能体平台
- 多通道智能体部署
- 智能体生命周期管理
- 自改进智能体系统

## 优势

- 完整的生产化能力
- 企业级安全和 RBAC
- 多通道分发
- 灵活部署（Docker、Railway、AWS、GCP）
