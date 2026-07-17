# tool/registry.py
from .calculator import calculator as calculator
from .time_tools import execute as time_tool
from .weather import execute as weather
from .air_quality import execute as air_quality
from .country_info import execute as country_info
from .sentiment import execute as sentiment
from .web_search import execute as web_search 
from .news import execute as news 

TOOLS = {
    "calculator": calculator,
    "time": time_tool,
    "weather": weather,
    "air_quality": air_quality,
    "country": country_info,
    "sentiment": sentiment,
    "web_search": web_search,
     "news": news,
}

def execute_tool(tool_name: str, arguments: dict):
    tool = TOOLS.get(tool_name)

    if tool is None:
        available = ', '.join(TOOLS.keys())
        return f"Unknown tool: {tool_name}. Available tools: {available}"
    
    return tool(arguments)

def list_tools():
    return list(TOOLS.keys())