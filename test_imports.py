# test_time.py
from agent import Agent

agent = Agent()

# Test time query
print("Testing time query:")
response = agent.run("What time is it?")
print(response)

print("\n" + "="*50 + "\n")

# Test multiple queries
print("Testing multiple queries:")
response = agent.run("What is 2+2 and what time is it?")
print(response)