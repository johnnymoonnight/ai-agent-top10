# CrewAI

**Stars**: 54,800+ | **语言**: Python | **许可证**: MIT

## 基本信息

- **仓库**: [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)
- **官网**: [https://crewai.com](https://crewai.com)
- **最新版本**: 1.15.1 (2026-06-27)
- **Forks**: 7,700+
- **认证开发者**: 100,000+
- **Used by**: 18,700+

## 简介

CrewAI 是一个快速灵活的多智能体自动化框架，用 Python 编写。它提供两种互补方式构建生产级多智能体应用：Crews（自主协作团队）和 Flows（事件驱动工作流）。支持角色扮演、工具集成、记忆、MCP/A2A 协议。超过 10 万开发者通过社区课程获得认证。

## 核心架构

- **Crews**: 自主协作智能体团队（角色、目标、工具、任务）
- **Flows**: 事件驱动工作流（状态、分支、路由）
- **YAML 配置**: 声明式智能体和任务配置
- **CrewAI AMP Suite**: 企业控制平面（可观测性、治理、安全）

## 快速开始

```bash
# 安装
uv pip install crewai

# 创建项目
crewai create crew my_project

# 运行
crewai run
```

## 配置文件示例

```yaml
# agents.yaml
researcher:
  role: "{topic} Senior Data Researcher"
  goal: "Uncover cutting-edge developments in {topic}"
  backstory: "You're a seasoned researcher..."

# tasks.yaml
research_task:
  description: "Conduct a thorough research about {topic}"
  expected_output: "A list with 10 bullet points"
  agent: researcher
```

## 使用场景

- 多智能体协作任务
- 自动化研究工作流
- 内容生成和分析
- 企业级智能体部署

## 优势

- YAML 声明式配置，上手简单
- Crews + Flows 双模式灵活
- 10万+ 认证开发者社区
- 企业级 AMP 套件
