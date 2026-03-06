from sqlalchemy import text
from tqdm import tqdm

from database.db import (
    get_db,
    insert_entity,
    insert_claim,
    insert_evidence
)

from extraction.extractor import extract_from_email
from extraction.validator import validate_extraction


LIMIT = 100


def run_extraction():

    with get_db() as db:

        result = db.execute(
            text(f"SELECT artifact_id, raw_text FROM artifacts LIMIT {LIMIT}")
        )

        emails = result.fetchall()

        print(f"Processing {len(emails)} emails")

        for artifact_id, raw_text in tqdm(emails):

            try:

                extraction = extract_from_email(raw_text)

                extraction = validate_extraction(extraction)

                for entity in extraction.entities:

                    insert_entity(db, entity.name, entity.type)

                for claim in extraction.claims:

                    subject_id = insert_entity(db, claim.subject, "Unknown")
                    object_id = insert_entity(db, claim.object, "Unknown")

                    claim_id = insert_claim(
                        db,
                        subject_id,
                        claim.predicate,
                        object_id
                    )

                    insert_evidence(
                        db,
                        claim_id,
                        artifact_id,
                        claim.evidence.excerpt
                    )

            except Exception as e:

                print("Extraction error:", e)


if __name__ == "__main__":
    run_extraction()