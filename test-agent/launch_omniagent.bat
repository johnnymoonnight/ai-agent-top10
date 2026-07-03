@echo off
title OmniAgent v0.2.0
cd /d "%~dp0"
echo ============================================
echo   OmniAgent v0.2.0 - AI Agent Framework
echo ============================================
echo.
echo Commands:
echo   think ^<task^>   - Agent thinks about a task
echo   chat ^<msg^>     - Send message to agent
echo   tools          - List available tools
echo   memory         - Show memory stats
echo   skills         - List builtin skills
echo   exit/quit      - Exit
echo.
:loop
set /p input="omniagent^> "
if /i "%input%"=="exit" goto :end
if /i "%input%"=="quit" goto :end
if /i "%input%"=="tools" python -c "from omniagent import ToolRegistry, WebSearch, CodeExecutor, FileSystem; t=ToolRegistry(); t.register(WebSearch()); t.register(CodeExecutor()); t.register(FileSystem()); [print(f'  - {x[\"name\"]}: {x[\"description\"]}') for x in t.list_tools()]"
if /i "%input%"=="memory" python -c "from omniagent import MemoryStore; m=MemoryStore(); print(m.consolidate())"
if /i "%input%"=="skills" python -c "from omniagent import SkillRegistry; s=SkillRegistry(); s.register_builtin_skills(); [print(f'  - {x.name}: {x.description}') for x in s.all]"
if /i "%input%"==" " goto :loop
echo %input%|findstr /b "think " >nul && (python -c "import asyncio; from omniagent import Agent, AgentConfig; a=Agent(AgentConfig(name='OmniAgent')); print(asyncio.run(a.think('%input%')))")
echo %input%|findstr /b "chat " >nul && (python -c "import asyncio; from omniagent import Agent, AgentConfig; a=Agent(AgentConfig(name='OmniAgent')); r=asyncio.run(a.think('%input%')); print('Response:', r)")
goto :loop
:end
echo Goodbye!
