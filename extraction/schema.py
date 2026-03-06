from dataclasses import dataclass
from typing import List


@dataclass
class Evidence:
    excerpt: str


@dataclass
class Claim:
    subject: str
    predicate: str
    object: str
    evidence: Evidence


@dataclass
class Entity:
    name: str
    type: str


@dataclass
class Extraction:
    entities: List[Entity]
    claims: List[Claim]