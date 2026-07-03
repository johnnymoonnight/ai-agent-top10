"""消息系统 - Agent间通信 (AutoGen/A2A模式)"""
from __future__ import annotations
import asyncio
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("omniagent.message")


class MessagePriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Message:
    source: str
    target: str
    content: Any
    msg_type: str = "text"
    priority: MessagePriority = MessagePriority.NORMAL
    metadata: Dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    msg_id: str = field(default_factory=lambda: f"msg_{datetime.now().timestamp()}")


class MessageBus:
    """消息总线 - AutoGen 分布式消息传递"""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._history: List[Message] = []
        self._queue: asyncio.Queue = asyncio.Queue()

    def subscribe(self, topic: str, handler: Callable):
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)

    def unsubscribe(self, topic: str, handler: Callable):
        if topic in self._subscribers:
            self._subscribers[topic] = [h for h in self._subscribers[topic] if h != handler]

    async def publish(self, message: Message):
        self._history.append(message)
        await self._queue.put(message)
        topic = message.msg_type
        for handler in self._subscribers.get(topic, []):
            try:
                await handler(message)
            except Exception as e:
                logger.error(f"Handler error: {e}")

    async def consume(self, timeout: Optional[float] = None) -> Optional[Message]:
        try:
            return await asyncio.wait_for(self._queue.get(), timeout)
        except asyncio.TimeoutError:
            return None

    def get_history(self, limit: int = 50) -> List[Message]:
        return self._history[-limit:]
