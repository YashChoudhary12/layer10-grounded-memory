from sqlalchemy import text
from database.db import get_db


def search_entity(name):

    with get_db() as db:

        result = db.execute(text("""
        SELECT
            e1.canonical_name AS subject,
            c.predicate,
            e2.canonical_name AS object,
            ev.excerpt
        FROM claims c
        JOIN entities e1 ON c.subject_entity = e1.entity_id
        JOIN entities e2 ON c.object_entity = e2.entity_id
        JOIN evidence ev ON ev.claim_id = c.claim_id
        WHERE e1.canonical_name ILIKE :name
        LIMIT 20
        """), {"name": f"%{name}%"})

        rows = result.fetchall()

        if not rows:
            print("No results found")
            return

        for row in rows:

            print("\nCLAIM")
            print(f"{row.subject} --{row.predicate}--> {row.object}")
            print("Evidence:", row.excerpt)


if __name__ == "__main__":

    while True:

        query = input("\nSearch entity (type 'exit' to quit): ")

        if query == "exit":
            break

        search_entity(query)