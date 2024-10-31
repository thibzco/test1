import streamlit as st


st.title("BP test")
#st.write("Hello from Streamlit!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# message = st.chat_message("assistant")
# message.write("Hello human")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User: {prompt}")