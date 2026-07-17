# tool/news.py
import requests
from datetime import datetime, timedelta

# Try to get API key from config
try:
    from config import NEWS_API_KEY
except:
    NEWS_API_KEY = "20f99f5f4a23401782fc4a089c83736b"

# GNews API (Free tier: 100 requests/day, no API key needed for limited use)
# Or use NewsAPI (requires API key)

def execute(arguments: dict):
    """
    Fetch latest news based on query or category
    """
    query = arguments.get("query")
    country = arguments.get("country", "us")  # Country code (us, in, gb, etc.)
    category = arguments.get("category", "general")  # general, business, technology, sports, health, science, entertainment
    max_results = arguments.get("max_results", 5)
    
    try:
        # Try with API key first
        if NEWS_API_KEY:
            return fetch_news_api(query, country, category, max_results)
        else:
            # Fallback to free GNews API (no key required)
            return fetch_gnews(query, country, category, max_results)
            
    except Exception as e:
        return f"News error: {e}"

def fetch_news_api(query, country, category, max_results):
    """Fetch news using NewsAPI (requires API key)"""
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "country": country,
            "category": category,
            "pageSize": max_results
        }
        
        if query:
            params["q"] = query
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] != "ok":
            return f"News API error: {data.get('message', 'Unknown error')}"
        
        articles = data.get("articles", [])
        
        if not articles:
            return "No news articles found"
        
        return format_news(articles, query, "NewsAPI")
        
    except Exception as e:
        return f"News API error: {e}"

def fetch_gnews(query, country, category, max_results):
    """Fetch news using GNews API (Free, no API key)"""
    try:
        url = "https://gnews.io/api/v4/top-headlines"
        params = {
            "country": country,
            "category": category,
            "max": max_results,
            "lang": "en"
        }
        
        if query:
            params["q"] = query
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        articles = data.get("articles", [])
        
        if not articles:
            return "No news articles found"
        
        return format_news(articles, query, "GNews")
        
    except Exception as e:
        return f"GNews error: {e}"

def format_news(articles, query, source):
    """Format news articles for display"""
    results = []
    
    if query:
        results.append(f"📰 News Results for: {query}")
    else:
        results.append(f"📰 Latest News ({source})")
    
    results.append("="*50)
    results.append("")
    
    for i, article in enumerate(articles, 1):
        title = article.get("title", "No title")
        description = article.get("description", article.get("content", ""))
        if description and len(description) > 200:
            description = description[:200] + "..."
        
        url = article.get("url", "#")
        source_name = article.get("source", {})
        if isinstance(source_name, dict):
            source_name = source_name.get("name", "Unknown")
        
        published = article.get("publishedAt", "")
        if published:
            try:
                dt = datetime.fromisoformat(published.replace('Z', '+00:00'))
                published = dt.strftime("%d-%m-%Y %H:%M")
            except:
                pass
        
        results.append(f"{i}. **{title}**")
        if description:
            results.append(f"   📝 {description}")
        if source_name:
            results.append(f"   📰 Source: {source_name}")
        if published:
            results.append(f"   🕐 {published}")
        results.append(f"   🔗 {url}")
        results.append("")
    
    return "\n".join(results)

if __name__ == "__main__":
    print("News Tool Testing")
    print("="*60)
    
    # Test with different queries
    test_cases = [
        {"query": "India"},
        {"country": "us", "category": "technology"},
        {"category": "business"},
    ]
    
    for test in test_cases:
        print(f"\nTesting: {test}")
        print("-"*40)
        result = execute(test)
        print(result)