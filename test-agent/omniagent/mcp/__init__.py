"""MCP协议集成 - Model Context Protocol 服务器与客户端"""
from __future__ import annotations
import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("omniagent.mcp")


@dataclass
class MCPTool:
    name: str
    description: str
    input_schema: Dict
    handler: Optional[Callable] = None


@dataclass
class MCPResource:
    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"


@dataclass
class MCPServer:
    name: str
    version: str = "1.0"
    tools: Dict[str, MCPTool] = field(default_factory=dict)
    resources: Dict[str, MCPResource] = field(default_factory=dict)


class MCPServerManager:
    """
    MCP 服务器管理器 - 200+ MCP服务器生态接入:
    - 文件系统、数据库、浏览器、开发工具
    - GitHub、Slack、Jira 等外部服务
    """

    def __init__(self):
        self.servers: Dict[str, MCPServer] = {}

    def register_server(self, server: MCPServer):
        self.servers[server.name] = server
        logger.info(f"MCP Server registered: {server.name}")

    def register_tool(self, server_name: str, tool: MCPTool):
        if server_name in self.servers:
            self.servers[server_name].tools[tool.name] = tool

    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict) -> Any:
        server = self.servers.get(server_name)
        if not server:
            return {"error": f"Server {server_name} not found"}
        tool = server.tools.get(tool_name)
        if not tool:
            return {"error": f"Tool {tool_name} not found on {server_name}"}
        if tool.handler:
            return await tool.handler(arguments)
        return {"status": "tool_registered", "server": server_name, "tool": tool_name}

    def list_servers(self) -> List[Dict]:
        return [{"name": s.name, "version": s.version,
                 "tools": list(s.tools.keys()),
                 "resources": list(s.resources.keys())}
                for s in self.servers.values()]

    def list_tools(self) -> List[Dict]:
        tools = []
        for s in self.servers.values():
            for t in s.tools.values():
                tools.append({"server": s.name, "name": t.name, "description": t.description})
        return tools
