# Top 10 AI Agent Frameworks on GitHub (2026)

> 全球排名前10的 AI 智能体框架/项目索引库
> 数据采集日期: 2026-07-02

---

## 索引

| # | 项目 | Stars | 语言 | 许可证 | 目录 |
|---|------|-------|------|--------|------|
| 1 | [AutoGPT](#1-autogpt) | 185k | Python | MIT / Polyform Shield | [详情](./projects/autogpt/) |
| 2 | [LangChain](#2-langchain) | 141k | Python | MIT | [详情](./projects/langchain/) |
| 3 | [MetaGPT](#3-metagpt) | 69.1k | Python | MIT | [详情](./projects/metagpt/) |
| 4 | [AutoGen (Microsoft)](#4-autogen-microsoft) | 59.4k | Python/C# | CC-BY-4.0 / MIT | [详情](./projects/autogen/) |
| 5 | [CrewAI](#5-crewai) | 54.8k | Python | MIT | [详情](./projects/crewai/) |
| 6 | [LlamaIndex](#6-llamaindex) | 50.6k | Python | MIT | [详情](./projects/llamaindex/) |
| 7 | [Agno](#7-agno) | 41k | Python | Apache-2.0 | [详情](./projects/agno/) |
| 8 | [Haystack](#8-haystack) | 25.8k | Python | Apache-2.0 | [详情](./projects/haystack/) |
| 9 | [Mastra](#9-mastra) | 25.7k | TypeScript | Apache-2.0 | [详情](./projects/mastra/) |
| 10 | [Vercel AI SDK](#10-vercel-ai-sdk) | 25.3k | TypeScript | Apache-2.0 | [详情](./projects/vercel-ai-sdk/) |

---

## 1. AutoGPT

[![Stars](https://img.shields.io/github/stars/Significant-Gravitas/AutoGPT)](https://github.com/Significant-Gravitas/AutoGPT)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://github.com/Significant-Gravitas/AutoGPT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

- **仓库**: [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)
- **官网**: [https://agpt.co](https://agpt.co)
- **Stars**: 185,000+
- **语言**: Python (69%), TypeScript (29.4%)
- **许可证**: MIT (核心) / Polyform Shield (平台)
- **最新版本**: autogpt-platform-beta-v0.6.65 (2026-06-25)

### 简介

AutoGPT 是最早也是最知名的自主 AI 智能体项目。它能够将用户定义的目标自动分解为子任务并顺序执行，实现了 LLM 调用的自主链式处理。AutoGPT 开创了自主智能体的范式，成为了智能体架构的参考实现。

### 核心功能

- **Agent Builder**: 低代码界面设计自定义 AI 智能体
- **Workflow Management**: 通过连接 Block 构建自动化工作流
- **Ready-to-Use Agents**: 预配置智能体库
- **Agent Protocol**: 标准化智能体通信协议
- **Forge**: 智能体应用开发工具包
- **Benchmark**: 智能体性能评测框架

### 使用场景

通用自主任务执行、智能体能力实验、自动化工作流编排

---

## 2. LangChain

[![Stars](https://img.shields.io/github/stars/langchain-ai/langchain)](https://github.com/langchain-ai/langchain)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://github.com/langchain-ai/langchain)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

- **仓库**: [langchain-ai/langchain](https://github.com/langchain-ai/langchain)
- **官网**: [https://docs.langchain.com/langchain/](https://docs.langchain.com/langchain/)
- **Stars**: 141,000+
- **语言**: Python (99.2%)
- **许可证**: MIT
- **最新版本**: langchain-core==1.4.8 (2026-06-18)

### 简介

LangChain 是构建 LLM 应用和 AI 智能体最流行的框架。它提供标准化的模型、嵌入、向量存储接口，以及 1000+ 预构建集成。LangChain 生态还包括 LangGraph（状态化多智能体编排）、Deep Agents（长时间运行工作流）和 LangSmith（可观测性平台）。

### 核心功能

- **标准化接口**: 统一的模型、嵌入、向量存储 API
- **模型互操作性**: 一行代码切换模型提供商
- **Chain/Agent 架构**: 模块化组件构建链和智能体
- **1000+ 集成**: 模型提供商、工具、向量数据库等
- **LangGraph**: 有状态的多智能体工作流
- **LangSmith**: 智能体评估和可观测性

### 使用场景

LLM 应用快速原型开发、RAG 系统、复杂多智能体编排、企业级 AI 应用

---

## 3. MetaGPT

[![Stars](https://img.shields.io/github/stars/FoundationAgents/MetaGPT)](https://github.com/FoundationAgents/MetaGPT)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://github.com/FoundationAgents/MetaGPT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

- **仓库**: [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)
- **官网**: [https://atoms.dev/](https://atoms.dev/)
- **Stars**: 69,100+
- **语言**: Python (97.5%)
- **许可证**: MIT
- **论文**: ICLR 2024, ICLR 2025 (AFlow, Oral Presentation)

### 简介

MetaGPT 是一个多智能体框架，模拟一家软件公司的运作。不同的智能体扮演产品经理、架构师、项目经理、工程师等角色，通过 SOP（标准操作流程）协作完成复杂任务。核心理念：代码 = SOP(团队)。

### 核心功能

- **多角色协作**: PM、架构师、工程师等角色分工
- **SOP 驱动**: 标准化操作流程
- **自然语言编程**: 一行需求输入 → 完整项目输出
- **Data Interpreter**: 数据分析智能体
- **MGX (MetaGPT X)**: 自然语言编程产品

### 使用场景

软件项目自动生成、多智能体协作研究、自然语言编程

---

## 4. AutoGen (Microsoft)

[![Stars](https://img.shields.io/github/stars/microsoft/autogen)](https://github.com/microsoft/autogen)
[![License: CC-BY-4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey)](https://github.com/microsoft/autogen)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

- **仓库**: [microsoft/autogen](https://github.com/microsoft/autogen)
- **官网**: [https://microsoft.github.io/autogen/](https://microsoft.github.io/autogen/)
- **Stars**: 59,400+
- **语言**: Python (61.7%), C# (25.1%), TypeScript (12.4%)
- **许可证**: CC-BY-4.0 (文档) / MIT (代码)
- **状态**: 维护模式（推荐使用 Microsoft Agent Framework）

### 简介

AutoGen 是微软研究院推出的多智能体对话系统框架。它支持构建可定制的多智能体应用，智能体可以自主行动或与人类协作。虽然已进入维护模式，但其架构设计和理念深远影响了整个智能体生态。

### 核心功能

- **Core API**: 消息传递、事件驱动智能体、分布式运行时
- **AgentChat API**: 快速原型开发的高层 API
- **Extensions API**: 第一/三方扩展
- **AutoGen Studio**: 无代码 GUI 构建多智能体应用
- **AutoGen Bench**: 智能体性能基准测试
- **Magentic-One**: 基于 AgentChat 的 SOTA 多智能体团队

### 使用场景

多智能体对话系统、人机协作、研究与教育

---

## 5. CrewAI

[![Stars](https://img.shields.io/github/stars/crewAIInc/crewAI)](https://github.com/crewAIInc/crewAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://github.com/crewAIInc/crewAI)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

- **仓库**: [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)
- **官网**: [https://crewai.com](https://crewai.com)
- **Stars**: 54,800+
- **语言**: Python
- **许可证**: MIT
- **最新版本**: 1.15.1 (2026-06-27)
- **认证开发者**: 100,000+

### 简介

CrewAI 是一个快速灵活的多智能体自动化框架。通过 Crews（自主协作团队）和 Flows（事件驱动工作流）两种互补方式构建生产级多智能体应用。支持角色扮演、工具集成、记忆和 MCP/A2A 协议。

### 核心功能

- **Crews**: 自主协作智能体团队
- **Flows**: 事件驱动的工作流引擎
- **YAML 配置**: 声明式智能体和任务配置
- **CrewAI AMP Suite**: 企业级控制平面
- **100+ 工具集成**: 内置丰富的工具生态
- **MCP/A2A 支持**: 开放协议集成

### 使用场景

多智能体协作、自动化工作流、研究分析、内容生成

---

## 6. LlamaIndex

[![Stars](https://img.shields.io/github/stars/run-llama/llama_index)](https://github.com/run-llama/llama_index)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](https://github.com/run-llama/llama_index)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

- **仓库**: [run-llama/llama_index](https://github.com/run-llama/llama_index)
- **官网**: [https://developers.llamaindex.ai](https://developers.llamaindex.ai)
- **Stars**: 50,600+
- **语言**: Python (72.4%), Jupyter Notebook (25%)
- **许可证**: MIT
- **300+ 集成**: LlamaHub 插件生态

### 简介

LlamaIndex 是领先的数据框架和文档智能体平台。它提供强大的数据连接器、索引/检索系统和查询接口，让 LLM 能够连接和利用私有数据。同时提供 LlamaParse（文档解析/OCR）、LlamaAgents（文档智能体）等企业服务。

### 核心功能

- **Data Connectors**: 100+ 数据源连接器
- **Indexing & Retrieval**: 多种索引和检索策略
- **LlamaParse**: 智能文档解析和 OCR
- **LlamaAgents**: 部署的文档智能体
- **Extract**: 结构化数据提取
- **RAG Pipeline**: 完整的检索增强生成管线

### 使用场景

文档智能处理、RAG 系统、知识库构建、企业数据智能化

---

## 7. Agno

[![Stars](https://img.shields.io/github/stars/agno-agi/agno)](https://github.com/agno-agi/agno)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue)](https://github.com/agno-agi/agno)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)

- **仓库**: [agno-agi/agno](https://github.com/agno-agi/agno)
- **官网**: [https://docs.agno.com](https://docs.agno.com)
- **Stars**: 41,000+
- **语言**: Python (99.7%)
- **许可证**: Apache-2.0
- **最新版本**: v2.6.20 (2026-06-26)

### 简介

Agno（原名 phidata）是构建、运行和管理智能体平台的 SDK。支持使用任何智能体框架构建智能体，作为生产服务运行（含追踪、调度、RBAC），通过统一控制面板管理。提供 100+ 集成和完整的可观测性。

### 核心功能

- **Production API**: 50+ 端点和 SSE/WebSocket 支持
- **100+ Integrations**: 预构建工具包
- **Context Providers**: 实时数据（Slack, Drive, MCP 等）
- **Human Approval**: 人工审批流程
- **RBAC**: JWT 角色权限控制
- **多通道**: Slack, Telegram, WhatsApp, Discord 等
- **可观测性**: OpenTelemetry 追踪

### 使用场景

企业级智能体平台、多通道智能体部署、智能体生命周期管理

---

## 8. Haystack

[![Stars](https://img.shields.io/github/stars/deepset-ai/haystack)](https://github.com/deepset-ai/haystack)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue)](https://github.com/deepset-ai/haystack)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)

- **仓库**: [deepset-ai/haystack](https://github.com/deepset-ai/haystack)
- **官网**: [https://haystack.deepset.ai](https://haystack.deepset.ai)
- **Stars**: 25,800+
- **语言**: Python, MDX
- **许可证**: Apache-2.0
- **最新版本**: v2.30.2 (2026-06-18)

### 简介

Haystack 是一个开源 AI 编排框架，用于构建生产级 LLM 应用。它提供模块化管道和智能体工作流，对检索、路由、记忆和生成有精确控制。支持 RAG、多模态应用、语义搜索和自主智能体。

### 核心功能

- **Modular Pipelines**: 模块化 AI 管道设计
- **Agent Workflows**: 智能体工作流
- **Model-Agnostic**: 支持 OpenAI、Mistral、Anthropic 等多模型
- **Hayhooks**: REST API / MCP 服务器部署
- **Enterprise Platform**: 托管部署方案
- **Telemetry**: 匿名使用统计

### 使用场景

生产级 RAG 系统、语义搜索、问答系统、企业 AI 应用

---

## 9. Mastra

[![Stars](https://img.shields.io/github/stars/mastra-ai/mastra)](https://github.com/mastra-ai/mastra)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue)](https://github.com/mastra-ai/mastra)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue)](https://typescriptlang.org)

- **仓库**: [mastra-ai/mastra](https://github.com/mastra-ai/mastra)
- **官网**: [https://mastra.ai](https://mastra.ai)
- **Stars**: 25,700+
- **语言**: TypeScript (99.2%)
- **许可证**: Apache-2.0 / Mastra Enterprise License
- **最新版本**: July 1, 2026

### 简介

Mastra 是现代 TypeScript 的 AI 应用和智能体框架。支持 40+ 模型提供商、内置工作流引擎、MCP 服务器、可观测性和评估工具。前端可集成 React/Next.js/Node.js。

### 核心功能

- **Model Router**: 40+ 模型提供商统一接口（3000+ 模型）
- **Agents**: 自主推理和工具调用
- **Workflows**: 图引擎工作流（.then()、.branch()、.parallel()）
- **Human-in-the-loop**: 暂停等待人工审批
- **MCP Server**: 编写 MCP 协议服务器
- **Observability**: 内置评估和可观测性
- **Context Management**: 对话历史、数据检索、记忆

### 使用场景

TypeScript 全栈 AI 应用、Next.js 智能体、MCP 服务器开发

---

## 10. Vercel AI SDK

[![Stars](https://img.shields.io/github/stars/vercel/ai)](https://github.com/vercel/ai)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue)](https://github.com/vercel/ai)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue)](https://typescriptlang.org)

- **仓库**: [vercel/ai](https://github.com/vercel/ai)
- **官网**: [https://ai-sdk.dev](https://ai-sdk.dev)
- **Stars**: 25,300+
- **语言**: TypeScript (80.5%)
- **许可证**: Apache-2.0
- **最新版本**: @ai-sdk/perplexity@3.0.42 (2026-07-02)

### 简介

Vercel AI SDK 是来自 Next.js 团队的 AI 工具包，支持 Next.js、React、Svelte、Vue、Angular 等主流框架。提供统一提供商架构、智能体（ToolLoopAgent）、结构化数据生成和丰富的 UI 集成。

### 核心功能

- **Unified Provider Architecture**: OpenAI、Anthropic、Google 等统一 API
- **ToolLoopAgent**: 工具循环智能体
- **generateText / generateObject**: 文本和结构化数据生成
- **UI Hooks**: useChat、useAssistant 等 React Hooks
- **Streaming**: 实时流式响应
- **Agent UI**: 智能体 UI 组件集成

### 使用场景

Web AI 应用、聊天机器人、智能体 UI、全栈 TypeScript AI

---

## 项目结构

```
ai-agent-top10/
├── README.md               # 本索引文件
├── projects/               # 各项目详情
│   ├── autogpt/
│   ├── langchain/
│   ├── metagpt/
│   ├── autogen/
│   ├── crewai/
│   ├── llamaindex/
│   ├── agno/
│   ├── haystack/
│   ├── mastra/
│   └── vercel-ai-sdk/
└── scripts/                # 辅助脚本
```

---

## 许可证

本仓库采用 MIT 许可证。各项目版权归各自所有者所有。

## 说明

Star 数据为 2026 年 7 月采集，可能与实时数据有偏差。
排名基于 GitHub Star 数量，仅供参考。
