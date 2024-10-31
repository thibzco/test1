import streamlit as st

st.write("Hello from Streamlit!")

message = st.chat_message("assistant")
message.write("Hello human")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")