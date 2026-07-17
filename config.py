# config.py
import os

# For deployment on Streamlit Cloud
try:
    import streamlit as st
    API_KEY = st.secrets.get("API_KEY", "")
except:
    API_KEY = os.getenv("API_KEY", "")

BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "llama-3.3-70b-versatile"