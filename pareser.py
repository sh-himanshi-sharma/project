import json
import re

def parse_tool_call(response: str):
    """Parse a single tool call from the response"""
    try:
        start_idx = response.find('{')
        end_idx = response.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = response[start_idx:end_idx]
            tool_request = json.loads(json_str)
            if isinstance(tool_request, dict) and "tool" in tool_request:
                return tool_request
    except Exception:
        pass
    return None

def parse_multiple_tool_calls(response: str):
    """Parse multiple tool calls from the response"""
    tool_calls = []
    try:
        # Method 1: Try to parse as JSON array first
        try:
            data = json.loads(response)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "tool" in item:
                        tool_calls.append(item)
                return tool_calls if tool_calls else None
        except:
            pass
        
        # Method 2: Find all JSON objects with "tool" key
        # Look for patterns like {"tool": "time"} or {"tool": "weather", "city": "Delhi"}
        pattern = r'\{[^{}]*"tool"[^{}]*\}'
        matches = re.findall(pattern, response)
        
        for match in matches:
            try:
                tool_request = json.loads(match)
                if isinstance(tool_request, dict) and "tool" in tool_request:
                    tool_calls.append(tool_request)
            except:
                continue
        
        # Method 3: If no JSON found, try to parse the whole response as one JSON
        if not tool_calls:
            try:
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end > start:
                    json_str = response[start:end]
                    data = json.loads(json_str)
                    if isinstance(data, dict) and "tool" in data:
                        tool_calls.append(data)
            except:
                pass
        
        return tool_calls if tool_calls else None
        
    except Exception:
        return None

if __name__ == "__main__":
    # Test cases
    test1 = '{"tool": "time"}'
    print("Test 1:", parse_multiple_tool_calls(test1))
    
    test2 = '{"tool": "time"} {"tool": "weather", "city": "Delhi"}'
    print("Test 2:", parse_multiple_tool_calls(test2))
    
    test3 = '[{"tool": "calculator", "expression": "2+2"}, {"tool": "time"}]'
    print("Test 3:", parse_multiple_tool_calls(test3))