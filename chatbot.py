import ollama
import streamlit as st
from utils.get_models import get_models
from utils.history import load_history, save_history
from datetime import datetime
from utils.stream_response import stream_response


def main():
    st.set_page_config(
        page_title="Ollama Chatbot", page_icon="🤖", initial_sidebar_state="expanded"
    )

    st.title("Ollama Chatbot")

    if "full_history" not in st.session_state:
        st.session_state.full_history = load_history()
        # Initialize active conversation ID if not present
        if "active_conversation_id" not in st.session_state:
            st.session_state.active_conversation_id = None

    with st.sidebar:
        st.markdown("## Conversations")

        # Option to start a new conversation
        if st.button("New Chat"):
            # Save the previous one if it exists and has messages
            if st.session_state.active_conversation_id and st.session_state.messages:
                st.session_state.full_history[
                    st.session_state.active_conversation_id
                ] = st.session_state.messages
                save_history(st.session_state.full_history)

            # Reset for the new conversation
            st.session_state.messages = []
            st.session_state.active_conversation_id = None
            st.rerun()

        # Select existing conversation
        conv_options = list(st.session_state.full_history.keys())
        # Display newer conversations first
        conv_options.sort(reverse=True)

        selected_conv_id = st.radio(
            "Load Conversation:",
            options=conv_options,
            key="conversation_selector",
            # index=None, # Default to no selection initially if no active_id
            # Set index if an active conversation is loaded
            index=conv_options.index(st.session_state.active_conversation_id)
            if st.session_state.active_conversation_id in conv_options
            else None,
            format_func=lambda x: x.replace("_", " ").split(".")[
                0
            ],  # Prettier display names
        )

        # Load selected conversation if different from active
        if (
            selected_conv_id
            and selected_conv_id != st.session_state.active_conversation_id
        ):
            # Save the previous one first (if applicable)
            if st.session_state.active_conversation_id and st.session_state.messages:
                st.session_state.full_history[
                    st.session_state.active_conversation_id
                ] = st.session_state.messages
                save_history(st.session_state.full_history)

            # Load the selected one
            st.session_state.active_conversation_id = selected_conv_id
            st.session_state.messages = st.session_state.full_history[selected_conv_id]
            st.rerun()  # Update the main chat display

        # Delete current conversation option
        if st.session_state.active_conversation_id:
            if st.button(
                f"🗑️ Delete Current Conversation ({st.session_state.active_conversation_id.replace('_', ' ').split('.')[0]})"
            ):
                if (
                    st.session_state.active_conversation_id
                    in st.session_state.full_history
                ):
                    del st.session_state.full_history[
                        st.session_state.active_conversation_id
                    ]
                    save_history(st.session_state.full_history)
                    st.session_state.active_conversation_id = None
                    st.session_state.messages = []
                    st.rerun()

        st.markdown("---")
        st.markdown("## Chat Options")
        MODEL = st.selectbox("Choose a model:", get_models())
        TEMP = st.slider("Choose the temperature: ", 0.0, 2.0, 0.7, 0.1)

    # Initialize chat history if it doesn't exist
    if "messages" not in st.session_state:
        if st.session_state.active_conversation_id:
            st.session_state.messages = st.session_state.full_history.get(
                st.session_state.active_conversation_id, []
            )
        else:
            st.session_state.messages = []

    # Display existing messages in the chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("What would you like to ask?")

    if user_input:
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Check if this is the first message of a new chat
        if st.session_state.active_conversation_id is None:
            st.session_state.active_conversation_id = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )
            # Add this new (empty) conversation to the full history temporarily
            # It will be properly saved after the assistant responds
            st.session_state.full_history[st.session_state.active_conversation_id] = []

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_input)

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

            # Save updated history
            if st.session_state.active_conversation_id:
                st.session_state.full_history[
                    st.session_state.active_conversation_id
                ] = st.session_state.messages
                save_history(st.session_state.full_history)
            # Rerun needed to update the conversation list in sidebar if it was a new chat
            if len(st.session_state.messages) == 2:  # User + Assistant = first turn
                st.rerun()

        except Exception as e:
            st.error(f"Error: {str(e)}")
            # Remove the user message if generation failed to prevent inconsistent state
            if (
                st.session_state.messages
                and st.session_state.messages[-1]["role"] == "user"
            ):
                st.session_state.messages.pop()


if __name__ == "__main__":
    main()
