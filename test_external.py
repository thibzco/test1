import streamlit as st


st.title("BP test")
#st.write("Hello from Streamlit!")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# message = st.chat_message("assistant")
# message.write("Hello human")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User: {prompt}")