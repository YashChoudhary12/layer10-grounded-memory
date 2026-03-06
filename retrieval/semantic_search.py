import ollama
from sqlalchemy import text
from database.db import get_db


def embed(text):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]


def semantic_search(query, top_k=5):

    query_vec = embed(query)

    with get_db() as db:

        result = db.execute(text("""
        SELECT
            e1.canonical_name AS subject,
            c.predicate,
            e2.canonical_name AS object,
            c.embedding <=> CAST(:query_vec AS vector) AS distance
        FROM claims c
        JOIN entities e1 ON c.subject_entity = e1.entity_id
        JOIN entities e2 ON c.object_entity = e2.entity_id
        ORDER BY c.embedding <=> CAST(:query_vec AS vector)
        LIMIT :top_k
        """), {
            "query_vec": query_vec,
            "top_k": top_k
        })

        rows = result.fetchall()

        for row in rows:
            print("\nMATCH")
            print(f"{row.subject} {row.predicate} {row.object}")
            print("distance:", row.distance)


if __name__ == "__main__":

    while True:
        q = input("\nAsk memory (or exit): ")

        if q.lower() == "exit":
            break

        semantic_search(q)