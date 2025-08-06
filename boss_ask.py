from openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
import os

st.title("老板问数助手(LangChain)")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

client = OpenAI(api_key=openai_api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Say something")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # Define the system prompt (modify as needed)
        filename = "prompt_text.txt"  # Replace with your text file name
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            system_prompt_content = file.read()

        system_prompt = {
            "role": "你是数据问答助手, 只回答与数据相关的问题",
            "content": system_prompt_content
        }

        # Combine system prompt with existing messages
        messages_for_api = [system_prompt] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]
    
        # Call OpenAI API with the updated messages
        stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=messages_for_api,  # Use the modified messages list
        stream=True,
    )
        response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})