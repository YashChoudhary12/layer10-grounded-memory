import ollama


def embed(text):

    text = text.lower().strip()

    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response["embedding"]