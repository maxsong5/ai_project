from openai import OpenAI
import streamlit as st

st.title("Boss-Ask-LangChain")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

client = OpenAI(api_key=openai_api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Say something and/or attach an image"
                       ,accept_file=True
                       ,file_type=["jpg", "jpeg", "png"])
if prompt and prompt.text:
    st.markdown(prompt.text)
    st.session_state.messages.append({"role": "user", "content": prompt.text})
if prompt and prompt["files"]:
    st.image(prompt["files"][0])
    st.session_state.messages.append({"role": "user", "content": prompt["files"][0]})


    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})