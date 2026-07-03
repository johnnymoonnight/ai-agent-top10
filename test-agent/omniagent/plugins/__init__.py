"""插件系统 - 可扩展架构"""
from __future__ import annotations
import importlib
import logging
from typing import Any, Dict, List, Optional, Type
from dataclasses import dataclass, field

logger = logging.getLogger("omniagent.plugins")


@dataclass
class PluginManifest:
    name: str
    version: str
    description: str
    author: str = ""
    dependencies: List[str] = field(default_factory=list)
    entry_point: str = ""


class PluginBase:
    """插件基类"""
    manifest: PluginManifest

    async def on_load(self, context: Dict) -> None: ...
    async def on_unload(self) -> None: ...
    async def on_before_task(self, task: str) -> Optional[str]: ...
    async def on_after_task(self, result: Dict) -> Optional[Dict]: ...


class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, PluginBase] = {}
        self._manifest: Dict[str, PluginManifest] = {}

    async def load_plugin(self, manifest: PluginManifest, plugin_class: Type[PluginBase]):
        if manifest.name in self._plugins:
            logger.warning(f"Plugin {manifest.name} already loaded")
            return
        instance = plugin_class()
        instance.manifest = manifest
        await instance.on_load({"timestamp": __import__("datetime").datetime.now().isoformat()})
        self._plugins[manifest.name] = instance
        self._manifest[manifest.name] = manifest
        logger.info(f"Loaded plugin: {manifest.name} v{manifest.version}")

    async def unload_plugin(self, name: str):
        plugin = self._plugins.get(name)
        if plugin:
            await plugin.on_unload()
            del self._plugins[name]
            del self._manifest[name]

    def get_plugin(self, name: str) -> Optional[PluginBase]:
        return self._plugins.get(name)

    def list_plugins(self) -> List[Dict]:
        return [{"name": m.name, "version": m.version, "description": m.description}
                for m in self._manifest.values()]
