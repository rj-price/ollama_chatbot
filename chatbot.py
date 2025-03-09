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
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{'role': 'user', 'content': user_input}]
        )
   
        st.markdown("**Assistant:**")
        st.write(response['message']['content'])
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
else:
    st.info("Enter a question to get started.")

