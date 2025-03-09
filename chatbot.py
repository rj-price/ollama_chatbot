import ollama
import streamlit as st

def get_models():
    models_dict = ollama.list()['models']
    models_num = len(models_dict)
    models_list = []
    for i in range(models_num):
        model = models_dict[i]['model']
        if 'latest' in model:
            models_list.append(model.split(':')[0])
        elif 'embed' in model:
            continue
        else:
            models_list.append(model)
    return models_list

def stream_response(stream):
    for chunk in stream:
        yield chunk['message']['content']
        

st.set_page_config(
    page_title="Ollama Chatbot",
    initial_sidebar_state="expanded"
)

with st.sidebar:   
    st.markdown("# Chat Options")
    MODEL = st.selectbox("Choose a model:", get_models())    


st.title("Ollama Chatbot")

user_input = st.text_input("Enter question: ", "")

if user_input:
    with st.spinner("Generating response..."):
        try:
            stream = ollama.chat(
                model=MODEL,
                messages=[{'role': 'user', 'content': user_input}],
                stream=True
            )
    
            st.markdown("**Assistant:**")
            st.write_stream(stream_response(stream))
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
else:
    st.info("Enter a question to get started.")



    