# LangChain

**Stars**: 141,000+ | **语言**: Python | **许可证**: MIT

## 基本信息

- **仓库**: [langchain-ai/langchain](https://github.com/langchain-ai/langchain)
- **官网**: [https://docs.langchain.com/langchain/](https://docs.langchain.com/langchain/)
- **最新版本**: langchain-core==1.4.8 (2026-06-18)
- **Forks**: 23,400+
- **Commits**: 16,363+

## 简介

LangChain 是构建 LLM 应用和 AI 智能体最流行的框架。提供标准化的模型、嵌入、向量存储接口，以及 1000+ 预构建集成。核心价值在于广度：团队可以一行代码切换模型提供商，从原型快速过渡到生产系统。

## 生态体系

- **LangChain Core**: 核心框架，Chains/Agents/Retrieval
- **LangGraph**: 有状态的多智能体编排框架
- **Deep Agents**: 长时间运行的高层智能体包
- **LangSmith**: 智能体评估和可观测性平台
- **LangSmith Deployment**: 智能体部署平台

## 核心功能

- 标准化模型/嵌入/向量存储接口
- 1000+ 预构建集成
- Chain/Agent 模块化组件
- RAG 管道构建
- 工具调用和函数调用
- 多智能体协作

## 快速开始

```python
# 安装
uv add langchain

# 使用
from langchain.chat_models import init_chat_model
model = init_chat_model("openai:gpt-5.5")
result = model.invoke("Hello, world!")
```

## 使用场景

- LLM 应用快速原型开发
- RAG 检索增强生成系统
- 复杂多智能体工作流
- 企业级 AI 应用
- 文档问答

## 优势

- 生态系统最大最完善
- 模型互操作性最强
- 社区活跃，资源丰富
- 从原型到生产的完整路径
