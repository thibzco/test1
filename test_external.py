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

if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("BP"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "BP", "content": response})