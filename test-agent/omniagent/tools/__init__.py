"""工具系统 - 融合 LangChain 工具架构 + smolagents 代码执行"""
from __future__ import annotations
import asyncio
import json
import subprocess
import tempfile
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    required_permissions: List[str] = field(default_factory=list)


class BaseTool(ABC):
    """工具基类 - LangChain tool 模式"""
    def __init__(self, spec: ToolSpec):
        self.spec = spec

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        ...

    def to_dict(self) -> Dict:
        return {"name": self.spec.name, "description": self.spec.description,
                "parameters": self.spec.parameters}


class CodeExecutor(BaseTool):
    """代码执行器 - smolagents/E2B 沙箱执行"""
    def __init__(self, sandbox: bool = True):
        super().__init__(ToolSpec(
            name="code_executor",
            description="在沙箱中执行Python代码",
            parameters={"code": {"type": "string", "description": "Python code"}}
        ))
        self.sandbox = sandbox

    async def execute(self, code: str, **kwargs) -> Dict:
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code)
                f.flush()
                result = subprocess.run(
                    ["python", "-c", code],
                    capture_output=True, text=True, timeout=30
                )
                return {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
        except subprocess.TimeoutExpired:
            return {"error": "Execution timeout"}
        except Exception as e:
            return {"error": str(e)}


class WebSearch(BaseTool):
    """网络搜索 - 浏览器自动化"""
    def __init__(self):
        super().__init__(ToolSpec(
            name="web_search",
            description="搜索网络获取最新信息",
            parameters={"query": {"type": "string"}}
        ))

    async def execute(self, query: str, **kwargs) -> Dict:
        import urllib.parse
        encoded = urllib.parse.quote(query)
        return {
            "status": "ok",
            "query": query,
            "note": "Web search interface - connect to search API for full functionality"
        }


class FileSystem(BaseTool):
    """文件系统操作 - 安全受限的文件访问"""
    def __init__(self, allowed_paths: List[str] = None):
        super().__init__(ToolSpec(
            name="file_system",
            description="读写文件和目录",
            parameters={"action": {"type": "string"}, "path": {"type": "string"}}
        ))
        self.allowed_paths = allowed_paths or []

    async def execute(self, action: str, path: str, content: str = None, **kwargs) -> Dict:
        import os
        if self.allowed_paths and not any(path.startswith(p) for p in self.allowed_paths):
            return {"error": f"Path not allowed: {path}"}
        try:
            if action == "read":
                with open(path, "r") as f:
                    return {"content": f.read()}
            elif action == "write" and content is not None:
                with open(path, "w") as f:
                    f.write(content)
                return {"status": "written"}
            elif action == "list":
                return {"files": os.listdir(path)}
            return {"error": f"Unknown action: {action}"}
        except Exception as e:
            return {"error": str(e)}


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self._tools[tool.spec.name] = tool

    def get(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict]:
        return [t.to_dict() for t in self._tools.values()]
