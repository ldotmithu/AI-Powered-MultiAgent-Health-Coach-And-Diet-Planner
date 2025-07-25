import streamlit as st
import requests
from streamlit_extras.add_vertical_space import add_vertical_space

# --- Config ---
st.set_page_config(page_title="AI Health & Fitness Assistant", page_icon="🏋️", layout="wide")
API_URL = "http://localhost:8000/chat"  # Change to deployed URL if needed

# --- Header Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fb;
    }
    .stChatInput textarea {
        height: 70px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏋️ AI Health & Fitness Assistant")
st.caption("Personalized workout & meal planning powered by AI 🤖")

# --- Sidebar ---
with st.sidebar:
    st.header("💡 Tips")
    st.markdown("- Ask for a **full body** or **lower body** workout.")
    st.markdown("- Try diet types like **vegan** or **vegetarian**.")
    st.markdown("- Use natural language like _“Give me a meal plan for weight loss”_")
    st.markdown("---")
    st.info("🔗 API Status: Live at `/chat`")
    add_vertical_space(2)
    st.markdown("Made with ❤️ using LangGraph, Streamlit & FastAPI")

# --- State Management ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_tool_calls" not in st.session_state:
    st.session_state.last_tool_calls = []  # Store latest tool calls

# --- Helper Function ---
def get_assistant_reply(message):
    try:
        with st.spinner("AI is thinking..."):
            res = requests.post(API_URL, json={"message": message})
            if res.status_code == 200:
                data = res.json()
                return data.get("messages", []), data.get("tool_calls", [])
            else:
                return [{"role": "assistant", "content": "⚠️ API error."}], []
    except Exception as e:
        return [{"role": "assistant", "content": f"❌ Request failed: {str(e)}"}], []

# --- Display Chat History ---
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# --- Chat Input ---
user_prompt = st.chat_input("Type your fitness or meal plan question here...")

if user_prompt:
    # Save user message
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Get AI response + tool call info
    assistant_messages, tool_calls = get_assistant_reply(user_prompt)

    # Save tool calls for sidebar display
    st.session_state.last_tool_calls = tool_calls

    # Display assistant reply
    for msg in assistant_messages:
        if msg["role"] == "assistant":
            st.session_state.chat_history.append(msg)
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

# --- Tool Call Debug Display in Sidebar ---
if st.session_state.last_tool_calls:
    with st.sidebar:
        st.markdown("### 🛠 Tool Calls Used")
        for i, call in enumerate(st.session_state.last_tool_calls):
            st.markdown(f"**{i+1}. Tool Name:** `{call['tool']}`")
            st.markdown(f"**Args:** `{call['args']}`")

            
