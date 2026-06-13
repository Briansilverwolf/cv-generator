from pydantic import BaseModel
from typing import Literal, Optional

from schema.ats import ATSAnalysis
from schema.cv import CVGenerationIR


class TemplateRegistry(BaseModel):
    available_slots: list[str]
    variants_by_slot: dict[str, list[str]]
    constraints: dict[str, str]


class TemplateSelection(BaseModel):
    slot: Literal[
        "minimal",
        "professional",
        "technical",
        "modern"
    ]
    variant: Literal[
        "compact",
        "detailed",
        "ats_friendly",
        "visual"
    ]
    version: Optional[str] = None




class CVState(BaseModel):
    
    upload: Optional[str] = None  # MarkItDown output

    # Intelligence layer
    analysis: Optional[ATSAnalysis] = None
    cv_ir: Optional[CVGenerationIR] = None

    # Presentation layer
    template_registry: Optional[TemplateRegistry] = None
    template: Optional[TemplateSelection] = None

    # Pipeline control
    stage: Literal[
        "uploaded",
        "analyzed",
        "structured",
        "templated",
        "rendered"
    ] = "uploaded"