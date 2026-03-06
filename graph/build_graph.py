from sqlalchemy import text
from database.db import get_db


def get_graph(limit=50):

    with get_db() as db:

        result = db.execute(text("""
        SELECT
            e1.canonical_name AS subject,
            c.predicate,
            e2.canonical_name AS object
        FROM claims c
        JOIN entities e1 ON c.subject_entity = e1.entity_id
        JOIN entities e2 ON c.object_entity = e2.entity_id
        LIMIT :limit
        """), {"limit": limit})

        edges = []

        for row in result:
            edges.append((row.subject, row.predicate, row.object))

        return edges


if __name__ == "__main__":

    edges = get_graph()

    for s, p, o in edges:
        print(f"{s} --{p}--> {o}")