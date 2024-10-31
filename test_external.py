import streamlit as st

st.write("Hello from Streamlit!")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
print("external python file")