CREATE TABLE artifacts (
    artifact_id TEXT PRIMARY KEY,
    artifact_type TEXT,
    source TEXT,
    author TEXT,
    raw_text TEXT,
    content_hash TEXT,
    created_at TIMESTAMP,
    metadata JSONB
);

CREATE TABLE entities (
    entity_id TEXT PRIMARY KEY,
    entity_type TEXT,
    canonical_name TEXT,
    created_at TIMESTAMP,
    metadata JSONB
);

CREATE TABLE entity_aliases (
    alias_id SERIAL PRIMARY KEY,
    entity_id TEXT REFERENCES entities(entity_id),
    alias TEXT
);

CREATE TABLE claims (
    claim_id TEXT PRIMARY KEY,
    subject_entity TEXT REFERENCES entities(entity_id),
    predicate TEXT,
    object_entity TEXT REFERENCES entities(entity_id),
    confidence FLOAT,
    valid_from TIMESTAMP,
    valid_until TIMESTAMP,
    extraction_version TEXT
);

CREATE TABLE evidence (
    evidence_id TEXT PRIMARY KEY,
    claim_id TEXT REFERENCES claims(claim_id),
    artifact_id TEXT REFERENCES artifacts(artifact_id),
    excerpt TEXT,
    char_start INT,
    char_end INT,
    timestamp TIMESTAMP
);

CREATE TABLE artifact_duplicates (
    duplicate_id SERIAL PRIMARY KEY,
    artifact_id TEXT,
    canonical_artifact_id TEXT
);

CREATE TABLE merge_logs (
    merge_id SERIAL PRIMARY KEY,
    entity_a TEXT,
    entity_b TEXT,
    canonical_entity TEXT,
    merge_reason TEXT,
    timestamp TIMESTAMP
);

CREATE TABLE extraction_versions (
    version_id TEXT PRIMARY KEY,
    model_name TEXT,
    prompt_version TEXT,
    schema_version TEXT,
    created_at TIMESTAMP
);