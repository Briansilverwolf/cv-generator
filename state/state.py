from pydantic import BaseModel
from typing import Literal, Optional,Any
from fastapi.responses import FileResponse
from markitdown import MarkItDown
import tempfile

from state.base import BaseState,CVState,CVStage
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

        
        return  state(
            upload=result.text_content,
            stage = CVStage.ANALYZE
        )
        
class AnalyzeState(BaseState):
    
    def handle(state:CVState):
        state.analysis = analyze_cv(
        state.upload
        )
        
        return state(
            stage=CVStage.CRAFT
        )
        
class CraftState(BaseState):
    
    def handle(state:CVState):
        
        state.cv_ir = write_cv(
                state.upload,
                state.analysis
            )
        return state(
            stage = CVStage.BUILD
        )
        
            
class BuildState(BaseState):
    
    
    def handle(state:CVState):     
        tree_builder = RenderTreeBuilder() 
        state.tree = tree_builder.build(
                        state.cv_ir
                    )
        return state(
            stage = CVStage.TEMPLATE
        )

class TemplateState(BaseState):
    
    def handle(state:CVStage,slot,variant):
        state.template = TemplateSelection(
                slot=slot,
                variant=variant
            )
        return CVStage(
            stage = CVStage.RENDER
        )
        
class RenderState(BaseState):
    
    def handle(state:CVState,type_:Literal["pdf","html"]):
        
        cv_renderer = CVRenderer()
        template_engine = TemplateEngine("template")
        
        
        rendered_html = template_engine.render(
            template=state.template,
            render_tree=state.tree.model_dump()
        )
        if type_ == "pdf":
            pdf_path = cv_renderer.render_pdf(
                rendered_html,
                temp=True
            )
            return FileResponse(
            path=pdf_path,
            media_type="application/pfd",
            filename="cv_server.pdf"
        )
        else:
            html_file =  cv_renderer.render_html(
                cv = rendered_html,
                temp =True
            )
            
            return FileResponse(
                path = html_file,
                media_type="appliction/html",
                filename = "cv_server.html"
            )
        
        return state(
            stage = CVStage.END
        )
    