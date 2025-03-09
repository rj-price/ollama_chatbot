# Ollama Chatbot

A simple, interactive web interface for chatting with Ollama language models using Streamlit.

## Overview

This application provides a user-friendly web interface to interact with local LLMs through the Ollama API. It features:

- A clean chat interface
- Model selection from available Ollama models
- Temperature adjustment for response generation
- Streaming responses
- Conversation history
- Option to start new conversations

## Requirements

- Python 3.7+
- Streamlit
- Ollama

## Installation

1. Ensure Ollama is installed and running on your system
   - Visit [Ollama's website](https://ollama.ai/) for installation instructions

2. Install the required Python packages:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Clone this repository or download the script.

## Usage

1. Start the application:
   ```bash
   streamlit run chatbot.py
   ```

2. Open your web browser and navigate to the URL displayed in your terminal (typically `http://localhost:8501`).

3. Use the sidebar to:
   - Select an Ollama model from those available on your system
   - Adjust the temperature setting (higher values = more creative responses)
   - Start a new conversation when needed

4. Type your message in the input box at the bottom of the chat interface.

## Features

- **Model Selection**: Dynamically lists available models from your Ollama installation
- **Temperature Control**: Adjust the randomness of responses
- **Streaming Responses**: See the model's response as it's being generated
- **Conversation History**: Your chat history is preserved during the session
- **Simple UI**: Clean, intuitive interface with minimal distractions

## Troubleshooting

- Ensure Ollama is running before starting the application
- If you encounter errors, they will be displayed in the chat interface
- Make sure your selected model is already pulled in Ollama

## Limitations

- The application maintains conversation history only for the current session
- There is no context window management, so long conversations may exceed model context limits
- Each message is treated independently (no conversation context is maintained between messages)
