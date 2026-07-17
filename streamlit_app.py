import streamlit as st
import sys
import traceback

# Page config
st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 AI Agent")
st.caption("Your AI Assistant with 6 Tools: Calculator, Time, Weather, Air Quality, Country Info, Sentiment Analysis")

# Initialize session state variables FIRST
if "agent" not in st.session_state:
    st.session_state.agent = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Try importing agent with error handling
try:
    from agent import Agent
    st.sidebar.success("✅ Agent loaded successfully")
    
    # Initialize agent if not already done
    if st.session_state.agent is None:
        try:
            st.session_state.agent = Agent()
            st.sidebar.success("✅ Agent initialized")
        except Exception as e:
            st.sidebar.error(f"❌ Failed to initialize Agent: {e}")
            st.session_state.agent = None
            
except ImportError as e:
    st.sidebar.error(f"❌ Failed to load Agent: {e}")
    st.sidebar.code(f"Import error: {e}\n\nPlease check that agent.py exists and all imports are correct.")

# Sidebar info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("This AI Agent can:")
    st.write("✅ Answer questions")
    st.write("✅ Perform calculations")
    st.write("✅ Get current time")
    st.write("✅ Get weather information")
    st.write("✅ Get air quality data")
    st.write("✅ Get country information")
    st.write("✅ Analyze sentiment of text")
    st.write("✅ Remember conversation")
    st.write("---")
    
    st.header("🔧 Available Tools")
    tools = ["Calculator", "Time", "Weather", "Air Quality", "Country Info", "Sentiment Analysis"]
    for tool in tools:
        st.write(f"• {tool}")
    st.write("---")
    
    # Show API status
    try:
        import config
        st.success(f"✅ API: {config.MODEL_NAME}")
    except:
        st.warning("⚠️ Config not found")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    # Show error if agent is None
    if st.session_state.agent is None:
        st.error("⚠️ Agent is not available. Check the error messages above.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    if st.session_state.agent is None:
        st.error("Agent is not available. Please check the error messages in the sidebar.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.agent.run(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})