import streamlit as st
import requests

API_URL = "http://backend:8000/chat"

st.set_page_config(page_title="Local ChatBot", page_icon="🤖")
st.title("🤖 Local ChatBot (Ollama)")

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": user_input, "history": st.session_state.history[:-1]},
                    timeout=60,
                )
                reply = response.json()["reply"]
            except Exception as e:
                reply = f"Error: {e}"
        st.write(reply)

    st.session_state.history.append({"role": "assistant", "content": reply})
