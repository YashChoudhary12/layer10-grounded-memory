import email
import hashlib
from pathlib import Path
import email.utils


def compute_hash(text):
    return hashlib.sha256(text.encode("utf-8", "ignore")).hexdigest()


def clean_text(text):
    """Remove binary and NUL characters"""
    if not text:
        return ""
    text = text.replace("\x00", "")
    text = text.encode("utf-8", "ignore").decode("utf-8", "ignore")
    return text


def extract_body(msg):
    """Safely extract body from email"""
    if msg.is_multipart():
        parts = []
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        parts.append(payload.decode(errors="ignore"))
                except Exception:
                    pass
        return "\n".join(parts)
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                return payload.decode(errors="ignore")
        except Exception:
            pass

    return ""


def parse_date(date_str):
    try:
        return email.utils.parsedate_to_datetime(date_str)
    except Exception:
        return None


def parse_email(file_path: Path):
    """Convert raw email → artifact"""

    try:
        with open(file_path, "r", errors="ignore") as f:
            msg = email.message_from_file(f)
    except Exception:
        return None

    body = extract_body(msg)
    raw_text = clean_text(body).strip()

    if not raw_text:
        return None

    artifact = {
        "artifact_id": compute_hash(str(file_path)),
        "artifact_type": "email",
        "source": "enron",
        "author": msg.get("From"),
        "raw_text": raw_text,
        "content_hash": compute_hash(raw_text),
        "created_at": parse_date(msg.get("Date")),
        "metadata": {
            "subject": msg.get("Subject"),
            "to": msg.get("To"),
            "file_path": str(file_path)
        }
    }

    return artifact