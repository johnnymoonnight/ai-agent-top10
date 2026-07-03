# LlamaIndex

**Stars**: 50,600+ | **语言**: Python | **许可证**: MIT

## 基本信息

- **仓库**: [run-llama/llama_index](https://github.com/run-llama/llama_index)
- **官网**: [https://developers.llamaindex.ai](https://developers.llamaindex.ai)
- **最新版本**: v0.14.23 (2026-06-24)
- **Forks**: 7,700+
- **Used by**: 24,400+

## 简介

LlamaIndex 是领先的数据框架和文档智能体平台。它提供强大的数据连接器、索引/检索系统和查询接口，让 LLM 能够连接和利用私有数据。同时还提供 LlamaParse（文档解析/OCR）、LlamaAgents（部署的文档智能体）等企业级服务。

## 核心功能

- **Data Connectors**: 连接 100+ 数据源和格式
- **Indexing**: 多种索引策略（向量、树、关键词等）
- **Retrieval**: 高级检索接口
- **Query Engine**: 灵活的查询引擎
- **LlamaParse**: 智能文档解析（130+ 格式）
- **LlamaAgents**: 文档智能体
- **Extract**: 结构化数据提取
- **300+ 集成**: LlamaHub 插件生态

## 快速开始

```python
# 安装
pip install llama-index-core

# 构建向量索引
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)

# 查询
query_engine = index.as_query_engine()
response = query_engine.query("你的问题")
```

## 使用场景

- 文档智能处理
- RAG 检索增强生成
- 企业知识库
- 文档问答系统
- 结构化数据提取

## 优势

- 数据连接器最丰富
- 300+ 集成插件生态
- 企业级文档解析能力
- 活跃的社区和文档
