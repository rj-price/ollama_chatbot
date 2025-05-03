def stream_response(stream):
    """Helper function to stream responses from Ollama."""
    for chunk in stream:
        yield chunk["message"]["content"]
