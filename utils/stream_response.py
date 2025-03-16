
def stream_response(stream):
    for chunk in stream:
        yield chunk['message']['content']
        