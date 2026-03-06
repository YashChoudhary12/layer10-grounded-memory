import ollama
import json
from extraction.schema import Extraction, Entity, Claim, Evidence


def extract_from_email(email_text):

    prompt = f"""
Extract entities and claims from the email.

Return JSON in this format:

{{
  "entities": [{{"name": "...", "type": "person|org|unknown"}}],
  "claims": [
    {{
      "subject": "...",
      "predicate": "...",
      "object": "...",
      "evidence": "text snippet"
    }}
  ]
}}

Email:
{email_text}
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    try:
        data = json.loads(content)
    except:
        return Extraction([], [])

    entities = [
        Entity(e["name"], e.get("type", "Unknown"))
        for e in data.get("entities", [])
    ]

    claims = [
        Claim(
            c["subject"],
            c["predicate"],
            c["object"],
            Evidence(c["evidence"])
        )
        for c in data.get("claims", [])
    ]

    return Extraction(entities, claims)