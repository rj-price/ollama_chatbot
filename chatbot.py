import ollama
import streamlit as st
from utils.get_models import get_models
from utils.stream_response import stream_response


def main():
    st.set_page_config(
        page_title="Ollama Chatbot", page_icon="🤖", initial_sidebar_state="expanded"
    )

    st.title("Ollama Chatbot")

    with st.sidebar:
        if st.button("New Conversation"):
            # Clear the existing message history
            st.session_state.messages = []
            st.rerun()

        st.markdown("# Chat Options")
        MODEL = st.selectbox("Choose a model:", get_models())
        TEMP = st.slider("Choose the temperature: ", 0.0, 2.0, 0.7, 0.1)

    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing messages in the chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("What would you like to ask?")

    if user_input:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    # Generate response using Ollama, passing the entire conversation history
                    stream = ollama.chat(
                        model=MODEL,
                        messages=st.session_state.messages,
                        options={"temperature": TEMP},
                        stream=True,
                    )
                    # Stream the response to the chat interface
                    chatbot_output = st.write_stream(stream_response(stream))

            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": chatbot_output}
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
