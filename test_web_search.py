# test_web_search.py
from tool.web_search import execute

# Test queries
queries = [
    "FIFA World Cup 2026",
    "who won the FIFA World Cup",
    "FIFA World Cup final",
]

for query in queries:
    print(f"\n{'='*50}")
    print(f"Testing: {query}")
    print('='*50)
    result = execute({"query": query})
    print(result)
    print('='*50)