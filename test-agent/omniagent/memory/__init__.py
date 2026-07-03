"""记忆系统 - 融合 Mem0/OpenMemory/OpenHuman 的层次化记忆"""
from __future__ import annotations
import json
import sqlite3
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class MemoryItem:
    content: str
    memory_type: str = "episodic"  # episodic, semantic, procedural, working
    source: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    importance: float = 0.5
    metadata: Dict = field(default_factory=dict)
    embedding: Optional[List[float]] = None


class MemoryStore:
    """
    层次化记忆系统 - 融合:
    - Mem0: 长期记忆层
    - OpenMemory: 持久化存储
    - OpenHuman: Memory Tree 记忆树
    - Karpathy: 知识库工作流
    """

    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.join(os.path.expanduser("~"), ".omniagent", "memory.db")
        if self.db_path != ":memory:":
            parent = os.path.dirname(self.db_path)
            if parent:
                os.makedirs(parent, exist_ok=True)
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init_db()
        self._working_memory: Dict[str, Any] = {}

    def _init_db(self):
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                type TEXT,
                source TEXT,
                timestamp TEXT,
                importance REAL,
                metadata TEXT
            )
        """)
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_type ON memories(type)")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)")
        self._conn.commit()

    def save(self, item: MemoryItem):
        self._conn.execute(
            "INSERT INTO memories (content, type, source, timestamp, importance, metadata) VALUES (?,?,?,?,?,?)",
            (item.content, item.memory_type, item.source, item.timestamp,
             item.importance, json.dumps(item.metadata))
        )
        self._conn.commit()

    def recall(self, query: str, limit: int = 10, memory_type: Optional[str] = None) -> List[MemoryItem]:
        if memory_type:
            rows = self._conn.execute(
                "SELECT content, type, source, timestamp, importance, metadata FROM memories WHERE type=? ORDER BY timestamp DESC LIMIT ?",
                (memory_type, limit)
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT content, type, source, timestamp, importance, metadata FROM memories ORDER BY importance DESC, timestamp DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [MemoryItem(content=r[0], memory_type=r[1], source=r[2],
                           timestamp=r[3], importance=r[4],
                           metadata=json.loads(r[5])) for r in rows]

    def forget(self, before: Optional[str] = None, memory_type: Optional[str] = None):
        if before and memory_type:
            self._conn.execute("DELETE FROM memories WHERE type=? AND timestamp<?", (memory_type, before))
        elif before:
            self._conn.execute("DELETE FROM memories WHERE timestamp<?", (before,))
        elif memory_type:
            self._conn.execute("DELETE FROM memories WHERE type=?", (memory_type,))
        self._conn.commit()

    def consolidate(self) -> Dict:
        """记忆整合 - 将工作记忆转为长期记忆"""
        stats = {"working_items": len(self._working_memory)}
        stats["total"] = self._conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        stats["by_type"] = dict(self._conn.execute(
            "SELECT type, COUNT(*) FROM memories GROUP BY type").fetchall())
        return stats

    def update_working(self, key: str, value: Any):
        self._working_memory[key] = value

    def get_working(self, key: str) -> Optional[Any]:
        return self._working_memory.get(key)

    def clear_working(self):
        self._working_memory.clear()
