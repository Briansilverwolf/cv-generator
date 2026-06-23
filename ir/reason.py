from __future__ import annotations

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# ============================================================
# CORE REASONING IR (UNIVERSAL CONTENT PLANNER)
# ============================================================


# ----------------------------
# INTENT
# ----------------------------

class Intent(BaseModel):
    """
    Defines why the content exists and what outcome it should achieve.
    """

    id: str = Field(..., description="Unique identifier for this intent instance.")

    goal: str = Field(
        ...,
        description="High-level objective of the content (free-form, domain-agnostic)."
    )

    audience: Optional[str] = Field(
        None,
        description="Target reader or user group the content is intended for."
    )

    context: Optional[str] = Field(
        None,
        description="Optional background context describing the situation or domain."
    )

    desired_outcome: Optional[str] = Field(
        None,
        description="Expected result after consuming the content."
    )

    constraints_hint: List[str] = Field(
        default_factory=list,
        description="Soft constraints or guiding signals influencing content creation."
    )


# ----------------------------
# CONTEXT
# ----------------------------

class ContextItem(BaseModel):
    """
    A single piece of contextual information used for reasoning.
    """

    type: Literal["user_input", "memory", "external", "instruction"] = Field(
        ...,
        description="Source type of the context item."
    )

    content: str = Field(
        ...,
        description="Raw contextual information used in reasoning."
    )

    confidence: float = Field(
        1.0,
        description="Confidence score (0.0–1.0) indicating reliability of the context item."
    )


class Context(BaseModel):
    """
    Collection of all contextual signals used during reasoning.
    """

    items: List[ContextItem] = Field(
        default_factory=list,
        description="List of all context items contributing to reasoning."
    )


# ----------------------------
# KNOWLEDGE GRAPH
# ----------------------------

class Node(BaseModel):
    """
    Atomic unit of meaning in the reasoning graph.
    """

    id: str = Field(
        ...,
        description="Unique identifier for the node."
    )

    type: Literal["concept", "entity", "claim", "event", "idea", "fact"] = Field(
        ...,
        description="Semantic classification of the node."
    )

    content: str = Field(
        ...,
        description="Core meaning or statement represented by the node."
    )


class Edge(BaseModel):
    """
    Relationship between two nodes in the knowledge graph.
    """

    source: str = Field(
        ...,
        description="ID of the source node."
    )

    target: str = Field(
        ...,
        description="ID of the target node."
    )

    relation: str = Field(
        ...,
        description="Type of relationship between nodes (free-form semantic link)."
    )


class KnowledgeGraph(BaseModel):
    """
    Structured representation of knowledge and relationships.
    """

    nodes: List[Node] = Field(
        default_factory=list,
        description="All reasoning nodes representing atomic units of meaning."
    )

    edges: List[Edge] = Field(
        default_factory=list,
        description="Relationships connecting nodes in the reasoning graph."
    )


# ----------------------------
# STRATEGY
# ----------------------------

class Strategy(BaseModel):
    """
    Defines how reasoning is applied to transform knowledge into structured output.
    """

    type: Literal[
        "explain",
        "persuade",
        "narrate",
        "compare",
        "instruct",
        "describe",
        "argue",
        "summarize"
    ] = Field(
        ...,
        description="Primary reasoning strategy guiding content transformation."
    )

    reasoning_path: List[str] = Field(
        default_factory=list,
        description="Step-by-step reasoning approach used to construct the output."
    )

    emphasis_nodes: List[str] = Field(
        default_factory=list,
        description="IDs of nodes that must be prioritized in final representation."
    )

    narrative_pressure: Optional[str] = Field(
        None,
        description="High-level instruction shaping tone, emphasis, or framing direction."
    )


# ----------------------------
# STRUCTURE
# ----------------------------

class StructureNode(BaseModel):
    """
    Logical grouping of knowledge graph nodes for downstream rendering.
    """

    id: str = Field(
        ...,
        description="Unique identifier for the structure node."
    )

    title: Optional[str] = Field(
        None,
        description="Optional human-readable label for the structure group."
    )

    purpose: str = Field(
        ...,
        description="Reason this group exists (e.g., grouping logic, dependency grouping, thematic clustering)."
    )

    node_ids: List[str] = Field(
        default_factory=list,
        description="List of KnowledgeGraph node IDs included in this structure group."
    )

    depends_on: List[str] = Field(
        default_factory=list,
        description="Other structure nodes this node depends on."
    )


class Structure(BaseModel):
    """
    High-level organization of reasoning outputs.
    """

    nodes: List[StructureNode] = Field(
        default_factory=list,
        description="Ordered or grouped structure nodes representing reasoning layout."
    )


# ----------------------------
# CONSTRAINTS
# ----------------------------

class Constraints(BaseModel):
    """
    Hard and soft constraints that influence final reasoning output.
    """

    max_length: Optional[int] = Field(
        None,
        description="Maximum allowed output length in tokens or words (if defined)."
    )

    tone: Optional[str] = Field(
        None,
        description="Desired communication tone (e.g., professional, neutral, technical)."
    )

    format_preferences: List[str] = Field(
        default_factory=list,
        description="Preferred output formatting styles or structural preferences."
    )

    must_include: List[str] = Field(
        default_factory=list,
        description="Elements that must appear in the final output reasoning structure."
    )

    must_avoid: List[str] = Field(
        default_factory=list,
        description="Elements that must be excluded from the final output."
    )


# ----------------------------
# FINAL REASONING IR
# ----------------------------

class ContentReasoningIR(BaseModel):
    """
    Universal content reasoning IR.

    Works across:
    - CVs
    - articles
    - stories
    - letters
    - tutorials
    - reports
    - documentation
    """

    intent: Intent = Field(
        ...,
        description="Core purpose and desired outcome of the content."
    )

    context: Context = Field(
        default_factory=Context,
        description="All external, inferred, and user-provided context signals."
    )

    knowledge_graph: KnowledgeGraph = Field(
        default_factory=KnowledgeGraph,
        description="Graph of atomic meaning units and their relationships."
    )

    strategy: Strategy = Field(
        ...,
        description="Reasoning strategy used to transform knowledge into structure."
    )

    structure: Structure = Field(
        ...,
        description="Logical grouping and organization of reasoning output."
    )

    constraints: Optional[Constraints] = Field(
        None,
        description="Constraints guiding formatting, tone, and content boundaries."
    )