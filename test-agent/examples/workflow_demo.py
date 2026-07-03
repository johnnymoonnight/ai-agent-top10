"""工作流示例"""
import asyncio
from omniagent import WorkflowEngine, WorkflowDefinition, WorkflowStep

async def step_a(ctx):
    print("Step A: processing...")
    ctx["data"] = "processed_by_A"
    return "A_done"

async def step_b(ctx):
    print(f"Step B: received {ctx.get('data')}")
    ctx["data2"] = "processed_by_B"
    return "B_done"

async def step_c(ctx):
    print(f"Step C: final step - {ctx.get('data')} -> {ctx.get('data2')}")
    return "C_done"

async def main():
    engine = WorkflowEngine()
    engine.register(WorkflowDefinition(
        name="test_workflow",
        steps={
            "A": WorkflowStep(name="A", action=step_a),
            "B": WorkflowStep(name="B", action=step_b, depends_on=["A"]),
            "C": WorkflowStep(name="C", action=step_c, depends_on=["B"]),
        }
    ))

    result = await engine.run("test_workflow")
    print(result["status"])

asyncio.run(main())
