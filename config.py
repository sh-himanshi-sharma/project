# config.py
import os

# API Keys
try:
    import streamlit as st
    API_KEY = st.secrets.get("API_KEY", "")
    FIRECRAWL_API_KEY = st.secrets.get("FIRECRAWL_API_KEY", "")
    NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "")
except:
    API_KEY = os.getenv("API_KEY", "")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")

# Fallback for local development (if secrets aren't set)
if not API_KEY:
    API_KEY = "your-groq-api-key-here"
if not FIRECRAWL_API_KEY:
    FIRECRAWL_API_KEY = "fc-c3596cae77e84ae0917f59ec0b266146"
if not NEWS_API_KEY:
    NEWS_API_KEY ="20f99f5f4a23401782fc4a089c83736b"

BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "llama-3.3-70b-versatile"