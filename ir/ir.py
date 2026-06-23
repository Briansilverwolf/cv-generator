from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional

# -----------------------------
# ENTITY
# -----------------------------

class Entity(BaseModel):
    id: str

    type: str

    name: str

    attributes: Dict[str, str] = Field(default_factory=dict)


# -----------------------------
# STATEMENT
# -----------------------------

class Statement(BaseModel):
    id: str

    content: str

    purpose: Literal[
        "inform",
        "describe",
        "persuade",
        "request",
        "narrate",
        "summarize"
    ]


# -----------------------------
# RELATIONSHIP
# -----------------------------

class Relationship(BaseModel):
    source: str

    target: str

    relation: str


# -----------------------------
# COLLECTION
# -----------------------------

class Collection(BaseModel):
    id: str

    collection_type: Literal[
        "list",
        "timeline",
        "comparison",
        "sequence",
        "examples"
    ]

    item_ids: List[str] = Field(default_factory=list)


# -----------------------------
# INTENT
# -----------------------------

class Intent(BaseModel):
    id: str

    goal: str

    related_item_ids: List[str] = Field(default_factory=list)


# -----------------------------
# SECTION
# -----------------------------

class Section(BaseModel):
    id: str

    purpose: str

    item_ids: List[str] = Field(default_factory=list)


# -----------------------------
# DOCUMENT
# -----------------------------

class Document(BaseModel):
    type: str

    sections: List[Section] = Field(default_factory=list)

    entities: List[Entity] = Field(default_factory=list)

    statements: List[Statement] = Field(default_factory=list)

    relationships: List[Relationship] = Field(default_factory=list)

    collections: List[Collection] = Field(default_factory=list)

    intents: List[Intent] = Field(default_factory=list)