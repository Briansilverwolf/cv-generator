from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Optional, Literal,List
from enum import Enum
from tempfile import NamedTemporaryFile

from schema.ats import ATSAnalysis
from schema.cv import CVGenerationIR
from template.registry import TemplateSelection,TemplateRegistry
from renders.builder import  RenderTree



class CVStage(Enum):
    UPLOAD = "upload"
    ANALYZE = "analyz"
    CRAFT = "crafted"
    BUILD = "structure"
    TEMPLATE= "template"
    RENDER = "render"
    END = "end"

class Render(BaseModel):
    id:int
    type_:str
    temp_path:NamedTemporaryFile


class CVState(BaseModel):
    upload: Optional[str] = None  # MarkItDown output
    analysis: Optional[ATSAnalysis] = None
    cv_ir: Optional[CVGenerationIR] = None
    tree: RenderTree= None
    template_registry: Optional[TemplateRegistry] = None
    template: Optional[TemplateSelection] = None
    renders:List[Render]
    stage: CVStage = CVStage.UPLOAD


class BaseState(ABC):
    @abstractmethod
    def handle(state:CVState)->CVState:
        pass
    
