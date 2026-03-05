from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os

# database connection string
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


from sqlalchemy import text

def insert_artifact(db, artifact):
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