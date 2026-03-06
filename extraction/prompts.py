EXTRACTION_PROMPT = """
We are extracting structured knowledge from corporate emails.

Return JSON with the following fields:

entities:
- name
- type (Person, Team, Project, Organization, Issue)

claims:
- subject
- predicate
- object
- evidence.excerpt

Email text:
----------------
{email_text}
----------------
"""