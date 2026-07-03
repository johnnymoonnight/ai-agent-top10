"""技能系统 - 融合 mattpocock/skills, addyosmani/agent-skills 框架"""
from __future__ import annotations
import importlib
import inspect
import logging
from typing import Any, Callable, Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("omniagent.skill")


@dataclass
class Skill:
    name: str
    description: str
    category: str = "general"
    version: str = "1.0"
    fn: Optional[Callable] = None
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class SkillRegistry:
    """
    技能注册表 - 融合:
    - mattpocock/skills: TDD, debugging, architecture
    - addyosmani/agent-skills: /spec, /plan, /build, /ship
    - anthropics/skills: 官方技能框架
    - Superpowers: agentic skills framework
    """

    def __init__(self):
        self._skills: Dict[str, Skill] = {}
        self._categories: Dict[str, List[str]] = {}

    def register(self, skill: Skill):
        self._skills[skill.name] = skill
        if skill.category not in self._categories:
            self._categories[skill.category] = []
        self._categories[skill.category].append(skill.name)

    def get(self, name: str) -> Optional[Skill]:
        return self._skills.get(name)

    def list_by_category(self, category: str) -> List[Skill]:
        return [self._skills[n] for n in self._categories.get(category, [])]

    def search(self, query: str) -> List[Skill]:
        q = query.lower()
        return [s for s in self._skills.values()
                if q in s.name.lower() or q in s.description.lower()]

    @property
    def all(self) -> List[Skill]:
        return list(self._skills.values())

    @property
    def categories(self) -> List[str]:
        return list(self._categories.keys())

    def register_builtin_skills(self):
        """注册内置技能 - 来自顶级项目的模式"""
        builtins = [
            Skill("plan", "制定详细执行计划", "planning", "2.0"),
            Skill("research", "联网搜索与研究", "research", "2.0"),
            Skill("code", "编写和审查代码", "development", "2.0"),
            Skill("debug", "调试与错误修复", "development", "2.0"),
            Skill("test", "编写和运行测试", "quality", "2.0"),
            Skill("review", "代码审查与改进建议", "quality", "2.0"),
            Skill("deploy", "部署到生产环境", "devops", "2.0"),
            Skill("document", "生成技术文档", "documentation", "2.0"),
            Skill("analyze", "数据分析与可视化", "analysis", "2.0"),
            Skill("architect", "系统架构设计", "planning", "2.0"),
            Skill("memory", "记忆管理与检索", "system", "2.0"),
            Skill("reflect", "自省与改进建议", "system", "2.0"),
        ]
        for s in builtins:
            self.register(s)


class SkillBase(Skill):
    """兼容别名 - 等同于 Skill"""
    pass
