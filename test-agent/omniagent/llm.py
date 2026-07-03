"""Mock LLM Provider - 本地最小可用模型用于测试"""
from __future__ import annotations
from typing import Any, Dict, List, Optional, Callable


class MockLLM:
    """Mock LLM - 返回预设响应，无需真实模型"""

    def __init__(self, responses: Optional[Dict[str, str]] = None):
        self.responses = responses or {}
        self.history: List[Dict] = []

    async def generate(self, prompt: str, **kwargs) -> str:
        self.history.append({"prompt": prompt, "kwargs": kwargs})
        for pattern, response in self.responses.items():
            if pattern in prompt:
                return response
        return f"Mock response to: {prompt[:50]}..."

    def register_response(self, pattern: str, response: str):
        self.responses[pattern] = response


class EchoLLM:
    """Echo LLM - 原样返回输入，用于工具调用测试"""

    async def generate(self, prompt: str, **kwargs) -> str:
        return prompt


class LLMProvider:
    """LLM Provider 适配层 - 可切换真实/模拟"""

    def __init__(self):
        self._backends: Dict[str, Any] = {}
        self._active: str = "mock"

    def register(self, name: str, backend: Any):
        self._backends[name] = backend

    def use(self, name: str):
        if name in self._backends:
            self._active = name

    async def generate(self, prompt: str, **kwargs) -> str:
        backend = self._backends.get(self._active)
        if not backend:
            return "No LLM backend active"
        return await backend.generate(prompt, **kwargs)
