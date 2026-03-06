from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from retrieval.embeddings import embed
from contextlib import contextmanager
import json


# PostgreSQL connection
DB_URL = "postgresql://localhost/layer10_memory"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# ARTIFACT INSERTION
# --------------------------------------------------

def insert_artifact(db, artifact):

    artifact["metadata"] = json.dumps(artifact["metadata"])

    query = text("""
        INSERT INTO artifacts (
            artifact_id,
            artifact_type,
            source,
            author,
            raw_text,
            content_hash,
            created_at,
            metadata
        )
        VALUES (
            :artifact_id,
            :artifact_type,
            :source,
            :author,
            :raw_text,
            :content_hash,
            :created_at,
            :metadata
        )
        ON CONFLICT (artifact_id) DO NOTHING
    """)

    db.execute(query, artifact)
    db.commit()


# --------------------------------------------------
# ENTITY INSERTION
# --------------------------------------------------

def insert_entity(db, name, entity_type):

    entity_id = name.lower().replace(" ", "_")

    query = text("""
        INSERT INTO entities (
            entity_id,
            entity_type,
            canonical_name
        )
        VALUES (
            :entity_id,
            :entity_type,
            :canonical_name
        )
        ON CONFLICT (entity_id) DO NOTHING
    """)

    db.execute(query, {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "canonical_name": name
    })

    db.commit()

    return entity_id


# --------------------------------------------------
# CLAIM INSERTION
# --------------------------------------------------

def insert_claim(db, subject, predicate, object_entity):

    claim_id = f"{subject}_{predicate}_{object_entity}"

    claim_text = f"{subject} {predicate} {object_entity}"

    # generate embedding
    embedding = embed(claim_text)

    query = text("""
        INSERT INTO claims (
            claim_id,
            subject_entity,
            predicate,
            object_entity,
            confidence,
            embedding
        )
        VALUES (
            :claim_id,
            :subject,
            :predicate,
            :object,
            :confidence,
            :embedding
        )
        ON CONFLICT (claim_id) DO NOTHING
    """)

    db.execute(query, {
        "claim_id": claim_id,
        "subject": subject,
        "predicate": predicate,
        "object": object_entity,
        "confidence": 0.8,
        "embedding": embedding
    })

    db.commit()

    return claim_id


# --------------------------------------------------
# EVIDENCE INSERTION
# --------------------------------------------------

def insert_evidence(db, claim_id, artifact_id, excerpt):

    evidence_id = f"{claim_id}_{artifact_id}"

    query = text("""
        INSERT INTO evidence (
            evidence_id,
            claim_id,
            artifact_id,
            excerpt
        )
        VALUES (
            :evidence_id,
            :claim_id,
            :artifact_id,
            :excerpt
        )
        ON CONFLICT (evidence_id) DO NOTHING
    """)

    db.execute(query, {
        "evidence_id": evidence_id,
        "claim_id": claim_id,
        "artifact_id": artifact_id,
        "excerpt": excerpt
    })

    db.commit()