# tool/web_search.py - Simple version
import requests
import os

try:
    from config import FIRECRAWL_API_KEY
except:
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")

def execute(arguments: dict):
    query = arguments.get("query")
    
    if not query:
        return "Web search error: No search query provided"
    
    try:
        # Direct API call using requests
        url = "https://api.firecrawl.dev/v1/search"
        headers = {
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "query": query,
            "limit": 3
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            return f"Search error: HTTP {response.status_code} - {response.text[:200]}"
        
        data = response.json()
        
        if "data" not in data or not data["data"]:
            return f"No results found for '{query}'"
        
        results = []
        results.append(f"🔍 Search Results for: {query}")
        results.append("="*50)
        results.append("")
        
        for i, result in enumerate(data["data"], 1):
            title = result.get("title", f"Result {i}")
            description = result.get("description", "No description available")
            url = result.get("url", "#")
            content = result.get("markdown", "")
            
            results.append(f"{i}. **{title}**")
            results.append(f"   {description[:300]}...")
            results.append(f"   🔗 {url}")
            
            if content:
                preview = content[:200].replace('\n', ' ').strip()
                if preview:
                    results.append(f"   📄 {preview}...")
            
            results.append("")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"Web search error: {e}"

if __name__ == "__main__":
    test_queries = [
        "FIFA World Cup 2026",
        "Who won the FIFA World Cup?",
        "Python programming",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        result = execute({"query": query})
        print(result)