from pydantic import BaseModel
from typing import Literal, Optional,Any
from fastapi.responses import FileResponse
from markitdown import MarkItDown
import tempfile

from state.base import BaseState,CVState,CVStage,Render
from renders.builder import RenderTreeBuilder
from renders.cv import CVRenderer
from renders.engine import TemplateEngine
from template.registry import TemplateSelection
from service import analyze_cv, write_cv
   


class UploadState(BaseState):  
    
    def handle(state:CVState,file):
        md = MarkItDown()
        content = file.file

        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        result = md.convert(tmp_path)      
        state.upload=result.text_content,
        state.stage = CVStage.ANALYZE
        return state
        
class AnalyzeState(BaseState):
    
    def handle(state:CVState):
        state.analysis = analyze_cv(state.upload)
        state.stage=CVStage.CRAFT
        return state  
        
class CraftState(BaseState):
    
    def handle(state:CVState):
        state.cv_ir = write_cv(state.upload,state.analysis)
        stage = CVStage.BUILD
        return state  
            
class BuildState(BaseState):
    
    def handle(state:CVState):     
        tree_builder = RenderTreeBuilder() 
        state.tree = tree_builder.build(state.cv_ir)
        stage = CVStage.TEMPLATE
        return state      

class TemplateState(BaseState):
    
    def handle(state:CVStage,slot,variant):
        state.template = TemplateSelection(slot=slot,variant=variant)
        stage = CVStage.RENDER
        return state
        
class RenderState(BaseState):
    
    def handle(state:CVState,type_:Literal["pdf","html"]):
        
        cv_renderer = CVRenderer()
        template_engine = TemplateEngine("template")
        
        
        rendered_html = template_engine.render(
            template=state.template,
            render_tree=state.tree.model_dump()
        )
        id = len(state.renders)
        
        if type_ == "pdf":
            pdf_path = cv_renderer.render_pdf(
                rendered_html,
                temp=True
            )
            
            state.renders.append(Render(
                id = id,
                type_="pdf",
                temp_path=pdf_path
            )
            )                                    
        else:
            html_path =  cv_renderer.render_html(
                cv = rendered_html,
                temp =True
            )
            
            state.renders.append(Render(
                id = id,
                type_="html",
                temp_path=html_path
            ))
            
        state.stage = CVStage.END
        return state      