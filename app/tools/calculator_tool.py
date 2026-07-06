# app/tools/calculator_tool.py

import math
from langchain_core.tools import tool


@tool
def calculator_tool(expression: str) -> str:
    """
    Evaluate a mathematical expression.

    Examples:
    - 10 + 20
    - 15 * 8
    - (10 + 5) * 2
    - 100 / 4
    """
    try:
        allowed_names = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
            "sqrt": math.sqrt,
            "ceil": math.ceil,
            "floor": math.floor,
            "pi": math.pi,
            "e": math.e,
        }

        result = eval(expression, {"__builtins__": {}}, allowed_names)
        print('result calculator',result)

        return str(result)

    except Exception as e:
        return f"Error: {e}"