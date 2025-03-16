import ollama
import streamlit as st
from utils.get_models import get_models
from utils.stream_response import stream_response

def main():
    st.set_page_config(
        page_title="Ollama Chatbot",
        page_icon="🤖",
        initial_sidebar_state="expanded"
    )

    st.title("Ollama Chatbot")
    
    with st.sidebar:
        if st.button("New Conversation"):
            st.session_state.messages = []
            st.rerun()   
        st.markdown("# Chat Options")
        MODEL = st.selectbox("Choose a model:", get_models())
        TEMP = st.slider("Choose the temperature: ", 0.0, 2.0, 0.7, 0.1)    

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    user_input = st.chat_input("What would you like to ask?")

    if user_input:
        try:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            st.session_state.messages.append({"role": "user", "content": user_input})
                
            with st.spinner("Generating response..."):
                stream = ollama.chat(
                    model=MODEL,
                    messages=[{'role': 'user', 'content': user_input}],
                    options={"temperature": TEMP},
                    stream=True
                )
                chatbot_output = st.write_stream(stream_response(stream))
                st.session_state.messages.append({"role": "assistant", "content": chatbot_output})
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
    