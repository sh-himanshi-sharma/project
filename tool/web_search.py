# tool/web_search.py - Using DuckDuckGo
import requests
from urllib.parse import quote

def execute(arguments: dict):
    query = arguments.get("query")
    
    if not query:
        return "Web search error: No search query provided"
    
    try:
        # DuckDuckGo Instant Answer API (free, no key)
        url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        
        # Get abstract/summary
        abstract = data.get("AbstractText", "")
        if abstract:
            results.append(f"Summary: {abstract}\n")
        
        # Get answer (for direct questions)
        answer = data.get("Answer", "")
        if answer:
            results.append(f"Answer: {answer}\n")
        
        # Get related topics
        topics = data.get("RelatedTopics", [])
        if topics:
            results.append("Related Topics:")
            for topic in topics[:5]:  # Limit to 5 results
                text = topic.get("Text", "")
                if text:
                    results.append(f"  • {text}")
        
        if not results:
            return f"No results found for '{query}'"
        
        return "\n".join(results)
        
    except requests.exceptions.Timeout:
        return "Web search error: Request timed out"
    except requests.exceptions.ConnectionError:
        return "Web search error: Could not connect to search service"
    except Exception as e:
        return f"Web search error: {e}"

if __name__ == "__main__":
    # Test the search
    test_queries = [
        "Python programming",
        "Who is the Prime Minister of India?",
        "Latest AI news",
        "What is machine learning?",
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print('='*50)
        result = execute({"query": query})
        print(result)