import streamlit as st
import json
import os

HISTORY_FILE = "chat_history.json"


def load_history():
    """Loads the chat history from the JSON file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                # Ensure file is not empty before loading
                if os.path.getsize(HISTORY_FILE) > 0:
                    return json.load(f)
                else:
                    return {}
        except (json.JSONDecodeError, FileNotFoundError):
            return {}  # Return empty if error or not found
    else:
        return {}


def save_history(history_data):
    """Saves the chat history to the JSON file."""
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history_data, f, indent=4)
    except IOError as e:
        st.error(f"Error saving history: {e}")
