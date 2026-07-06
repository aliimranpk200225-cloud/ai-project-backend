# app/tools/time_tool.py

from datetime import datetime
from langchain_core.tools import tool


@tool
def time_tool() -> str:
    """
    Returns the current local date and time.

    Use this tool when the user asks:
    - What time is it?
    - What's today's date?
    - Current time
    - Current date
    """
    print('result date','result date')
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")