# Vercel AI SDK

**Stars**: 25,300+ | **语言**: TypeScript | **许可证**: Apache-2.0

## 基本信息

- **仓库**: [vercel/ai](https://github.com/vercel/ai)
- **官网**: [https://ai-sdk.dev](https://ai-sdk.dev)
- **最新版本**: @ai-sdk/perplexity@3.0.42 (2026-07-02)
- **Forks**: 4,700+
- **Used by**: 98,600+
- **Releases**: 20,800+

## 简介

Vercel AI SDK 是来自 Vercel/Next.js 团队的 AI 工具包，支持 Next.js、React、Svelte、Vue、Angular 等主流框架。提供统一提供商架构、智能体（ToolLoopAgent）、结构化数据生成和丰富的 UI 集成。是 TypeScript 生态中最流行的 AI 开发工具。

## 核心功能

- **Unified Provider Architecture**: 统一 API 调用多模型提供商
- **ToolLoopAgent**: 工具循环智能体
- **generateText / generateObject**: 文本和结构化数据生成
- **UI Hooks**: useChat、useAssistant 等框架 Hooks
- **Streaming**: 实时流式响应
- **Agent UI**: 智能体 UI 组件集成
- **Structured Output**: Zod Schema 结构化输出

## 快速开始

```bash
npm install ai
```

## 核心用法

```typescript
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'openai/gpt-5.4',
  prompt: 'What is an agent?',
});
```

## 使用场景

- Web AI 应用开发
- 聊天机器人和对话 UI
- 智能体 UI 组件
- 全栈 TypeScript AI

## 优势

- 98,600+ 项目使用
- 框架无关的 UI 集成
- 20,000+ 版本迭代
- Vercel 生态深度集成
