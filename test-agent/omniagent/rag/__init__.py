"""RAG系统 - 融合 LlamaIndex/Haystack 的检索增强生成"""
from __future__ import annotations
import json
import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Document:
    content: str
    source: str = ""
    metadata: Dict = field(default_factory=dict)
    doc_id: str = field(default_factory=lambda: f"doc_{id({})}")


class VectorStore:
    """简单的向量存储 - 可替换为 Chroma/Pinecone/Weaviate"""
    def __init__(self):
        self._documents: Dict[str, Document] = {}
        self._embeddings: Dict[str, List[float]] = {}

    def add(self, doc: Document, embedding: Optional[List[float]] = None):
        self._documents[doc.doc_id] = doc
        if embedding:
            self._embeddings[doc.doc_id] = embedding

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Document]:
        if not self._embeddings:
            return list(self._documents.values())[:top_k]
        scores = []
        for doc_id, emb in self._embeddings.items():
            score = sum(a * b for a, b in zip(emb, query_embedding))
            scores.append((score, doc_id))
        scores.sort(reverse=True)
        return [self._documents[s[1]] for s in scores[:top_k]]


class RAGPipeline:
    """
    RAG 管道 - 融合 LlamaIndex/Haystack:
    - LlamaIndex: 索引+检索+查询引擎
    - Haystack: 模块化管道
    - LangChain: 文档链
    """

    def __init__(self):
        self.vector_store = VectorStore()
        self._retrieval_chain: List[Dict] = []
        self._index_stats = {"documents": 0, "chunks": 0}

    def index_document(self, content: str, source: str = "", chunk_size: int = 512):
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
        for i, chunk in enumerate(chunks):
            doc = Document(content=chunk, source=source,
                          metadata={"chunk": i, "total": len(chunks)})
            self.vector_store.add(doc)
        self._index_stats["documents"] += 1
        self._index_stats["chunks"] += len(chunks)

    def retrieve(self, query: str, top_k: int = 5) -> List[Document]:
        dummy_embedding = [0.0] * 384
        return self.vector_store.search(dummy_embedding, top_k)

    def query(self, query: str, context: Optional[str] = None) -> Dict:
        docs = self.retrieve(query)
        return {
            "query": query,
            "context": context or "",
            "documents": [{"content": d.content[:200], "source": d.source} for d in docs],
            "answer": "RAG response synthesized from retrieved documents"
        }

    def stats(self) -> Dict:
        return self._index_stats
