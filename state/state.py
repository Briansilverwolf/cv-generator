from pydantic import BaseModel
from typing import Literal, Optional,Any

from schema.ats import ATSAnalysis
from schema.cv import CVGenerationIR
from template.registry import TemplateSelection
from renders import RenderTreeBuilder


class TemplateRegistry(BaseModel):
    available_slots: list[str]
    variants_by_slot: dict[str, list[str]]
    constraints: dict[str, str]

class CVState(BaseModel):
    
    upload: Optional[str] = None  # MarkItDown output

    # Intelligence layer
    analysis: Optional[ATSAnalysis] = None
    tree: Any= None
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