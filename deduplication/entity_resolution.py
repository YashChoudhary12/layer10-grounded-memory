from sqlalchemy import text
from database.db import get_db
from rapidfuzz import fuzz


SIMILARITY_THRESHOLD = 90


def get_entities():

    with get_db() as db:

        result = db.execute(text("""
        SELECT entity_id, canonical_name
        FROM entities
        """))

        return result.fetchall()


def merge_entities(source_id, target_id):

    with get_db() as db:

        # Update claims
        db.execute(text("""
        UPDATE claims
        SET subject_entity = :target
        WHERE subject_entity = :source
        """), {"target": target_id, "source": source_id})

        db.execute(text("""
        UPDATE claims
        SET object_entity = :target
        WHERE object_entity = :source
        """), {"target": target_id, "source": source_id})

        # Remove duplicate entity
        db.execute(text("""
        DELETE FROM entities
        WHERE entity_id = :source
        """), {"source": source_id})

        db.commit()


def run_deduplication():

    entities = get_entities()

    for i in range(len(entities)):

        id1, name1 = entities[i]

        for j in range(i + 1, len(entities)):

            id2, name2 = entities[j]

            score = fuzz.ratio(name1.lower(), name2.lower())

            if score > SIMILARITY_THRESHOLD:

                print(f"Merging {name2} → {name1}")

                merge_entities(id2, id1)


if __name__ == "__main__":
    run_deduplication()