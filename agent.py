from llm import chat
from memory import load_memory, save_memory
from prompts import SYSTEM_PROMPT
from pareser import parse_tool_call, parse_multiple_tool_calls
from tool.registery import execute_tool

class Agent:

    def run(self, user_input: str) -> str:

        memory = load_memory()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages.extend(memory)

        messages.append({
            "role": "user",
            "content": user_input
        })

        llm_response = chat(messages)
        print(f"LLM Response: {llm_response}")

        # Check for multiple tool calls
        tool_calls = parse_multiple_tool_calls(llm_response)
        
        if tool_calls and len(tool_calls) > 1:
            print("="*50)
            print("MULTIPLE TOOLS REQUESTED")
            print("="*50)
            
            tool_results = []
            for tool_request in tool_calls:
                tool_name = tool_request.get("tool")
                arguments = tool_request.copy()
                arguments.pop("tool", None)
                
                print(f"Tool: {tool_name}")
                print(f"Arguments: {arguments}")
                
                tool_result = execute_tool(tool_name, arguments)
                tool_results.append(f"{tool_name} result: {tool_result}")
                print(f"Result: {tool_result}")
            
            combined_result = "\n".join(tool_results)
            print("="*50)
            
            messages.append({
                "role": "assistant",
                "content": llm_response
            })
            
            messages.append({
                "role": "user",
                "content": f"""
                Tool Results:
                {combined_result}
                Using these results, answer the user's original question in a natural, conversational way.
                Don't mention the tool calls or JSON. Just give the answer directly.
                """
            })
            
            final_response = chat(messages)
            
            memory.append({
                "role": "user",
                "content": user_input
            })
            
            memory.append({
                "role": "assistant",
                "content": final_response
            })
            
            save_memory(memory)
            return final_response
        
        # Check for single tool call
        tool_request = parse_tool_call(llm_response)

        if tool_request is None:
            memory.append({
                "role": "user",
                "content": user_input
            })

            memory.append({
                "role": "assistant",
                "content": llm_response
            })

            save_memory(memory)
            return llm_response
        
        print("="*50)
        print("TOOL REQUESTED")
        print("="*50)

        tool_name = tool_request.get("tool")
        arguments = tool_request.copy()
        arguments.pop("tool", None)

        print(f"Tool: {tool_name}")
        print(f"Arguments: {arguments}")

        tool_result = execute_tool(
            tool_name,
            arguments
        )

        print(f"Result: {tool_result}")
        print("="*50)

        messages.append({
            "role": "assistant",
            "content": llm_response
        })

        messages.append({
            "role": "user",
            "content": f"""
            Tool Result: {tool_result}
            Using this result, answer the user's original question in a natural, conversational way.
            Don't mention the tool calls or JSON. Just give the answer directly.
            
            For time queries, say something like "The current time is [time]" or "It is [time]".
            For weather queries, say something like "The weather in [city] is [temperature] with [conditions]".
            For sentiment queries, say something like "The sentiment is [positive/negative/neutral]".
            """
        })

        final_response = chat(messages)

        memory.append({
            "role": "user",
            "content": user_input
        })

        memory.append({
            "role": "assistant",
            "content": final_response
        })

        save_memory(memory)

        return final_response