from pydantic import BaseModel


class TemplateDefinition(BaseModel):
    name: str
    layout_path: str
    
from pydantic import BaseModel
from typing import Literal, Optional


class TemplateRegistry(BaseModel):
    available_slots: list[str]
    variants_by_slot: dict[str, list[str]]
    constraints: dict[str, str]

class TemplateSelection(BaseModel):
    
    slot: Literal[
        "minimal",
        "professional",
        "technical",
        "modern",
        "ats"
    ]

    variant: Literal[
        "obsidian",
        "swiss_grid",
        "blueprint",
        "manuscript",
        "broadsheet",
        "studio",
        "compact",
        "detailed",
        "ats",
        "visual"
    ]

    # optional control for future experimentation
    version: Optional[str] = None

MAPPING= {
            "compact": "styles/compact.css",
            "detailed": "styles/detailed.css",
            "ats": "styles/ats.css",
            "visual": "styles/detailed.css",
            "manuscript":"styles/manuscript.css",
            "obsidian":"styles/obsidian.css",
            "swiss_grid":"styles/swiss_grid.css",
            "blueprint":"styles/blueprint.css",
            "broadsheet":"styles/broadsheet.css",
            "studio":"styles/studio.css"
        }

TEMPLATES = {
    "professional": TemplateDefinition(
        name="professional",
        layout_path="/professional/layout.html"
    ),

    "modern": TemplateDefinition(
        name="modern",
        layout_path="/modern/layout.html"
    ),

    "ats": TemplateDefinition(
        name="ats",
        layout_path="/ats/layout.html"
    ),
}