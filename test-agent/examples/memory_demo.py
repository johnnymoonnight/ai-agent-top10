"""记忆系统示例"""
from omniagent import MemoryStore, MemoryItem

def main():
    mem = MemoryStore(db_path=":memory:")
    mem.save(MemoryItem(content="User likes Python", memory_type="semantic", importance=0.9))
    mem.save(MemoryItem(content="Completed task X", memory_type="episodic", importance=0.7))
    mem.update_working("current_project", "OmniAgent")

    results = mem.recall("user", limit=5)
    for r in results:
        print(f"[{r.memory_type}] {r.content}")

    print(f"Working memory: {mem.get_working('current_project')}")
    print(f"Stats: {mem.consolidate()}")

main()
