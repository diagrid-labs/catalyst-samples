from __future__ import annotations

from dapr_agents import DurableAgent, tool
from dapr_agents.workflow.runners import AgentRunner

def _normalize_number(value: float) -> int | float:
    rounded = round(value, 10)
    return int(rounded) if rounded.is_integer() else rounded

@tool
def add(a: float, b: float) -> int | float:
    """Add two numbers."""
    return _normalize_number(a + b)

@tool
def subtract(a: float, b: float) -> int | float:
    """Subtract `b` from `a`."""
    return _normalize_number(a - b)

@tool
def multiply(a: float, b: float) -> int | float:
    """Multiply two numbers."""
    return _normalize_number(a * b)

@tool
def divide(a: float, b: float) -> int | float:
    """Divide `a` by `b`."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return _normalize_number(a / b)

def main() -> None:
    runner = AgentRunner()
    agent = DurableAgent(
        name="Calculator",
        role="Line Graph Calculator",
        goal="Solve arithmetic and straight-line graph questions accurately.",
        instructions=[
            "Always use the provided tools for arithmetic instead of mental math.",
            "For straight-line graph questions, calculate slope as (y2 - y1) / (x2 - x1).",
            "If asked for the value of y at a given x, derive the line equation from the known points and evaluate it step by step with tools.",
            "Return a concise answer with the key working and the final result.",
        ],
        tools=[add, subtract, multiply, divide],
    )

    try:
        runner.subscribe(agent, await_result=True, log_outcome=True)
        runner.serve(agent, port=8001)
    finally:
        runner.shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
