"""RAG管道示例"""
from omniagent import RAGPipeline

def main():
    rag = RAGPipeline()
    rag.index_document(
        "OmniAgent is a meta-agent framework that integrates top 10 AI agent frameworks.",
        source="docs/intro.md"
    )
    rag.index_document(
        "Key features: multi-agent orchestration, skill system, memory, workflow, MCP, RAG.",
        source="docs/features.md"
    )

    result = rag.query("What is OmniAgent?")
    print(f"Query: {result['query']}")
    for doc in result["documents"]:
        print(f"  - [{doc['source']}] {doc['content'][:60]}...")

main()
