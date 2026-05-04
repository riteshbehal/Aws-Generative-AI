# chatbot_frontend.py

import streamlit as st
import chatbot_backend as demo

# Title
st.title("🤖 Bedrock Chatbot")

# Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = demo.get_memory()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.chat_history.append({
        "role": "user",
        "text": user_input
    })

    # Generate response
    response = demo.generate_response(
        input_text=user_input,
        memory=st.session_state.memory
    )

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.chat_history.append({
        "role": "assistant",
        "text": response
    })