from pathlib import Path
from tqdm import tqdm
import sys

sys.path.append(".")

from database.db import get_db, insert_artifact
from ingestion.email_parser import parse_email


DATASET_PATH = Path("data/raw/enron_mail/maildir")


def ingest_dataset():

    files = list(DATASET_PATH.rglob("*"))

    # ignore hidden/system files
    email_files = [
        f for f in files
        if f.is_file() and not f.name.startswith(".")
    ]

    # limit dataset for development
    email_files = email_files[:10000]

    print(f"Found {len(email_files)} email files")

    with get_db() as db:

        for file_path in tqdm(email_files):

            artifact = parse_email(file_path)

            if artifact is None:
                continue

            try:
                insert_artifact(db, artifact)
            except Exception as e:
                print(f"Error inserting {file_path}: {e}")


if __name__ == "__main__":
    ingest_dataset()