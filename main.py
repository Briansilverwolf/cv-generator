from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)

from llm import model
from utils.extract import aextract_file
from service import analyze_cv, write_cv
from renders import (
    CVRenderer,
    RenderTreeBuilder,
    TemplateEngine
)
from template.registry import TemplateSelection
from state import CVState


# ==========================================================
# MODELS
# ==========================================================

class Query(BaseModel):
    request: str


class TemplateRequest(BaseModel):
    slot: str
    variant: str


# ==========================================================
# APP SETUP
# ==========================================================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# GLOBAL OBJECTS
# ==========================================================

state = CVState(
    template=TemplateSelection(
        slot="professional",
        variant="studio"
    )
)

cv_renderer = CVRenderer()
tree_builder = RenderTreeBuilder()
template_engine = TemplateEngine("template")


# ==========================================================
# HELPERS
# ==========================================================

async def render_current_template() -> str:

    if state.tree is None:
        raise HTTPException(
            status_code=400,
            detail="No CV has been generated yet."
        )

    rendered_html = template_engine.render(
        template=state.template,
        render_tree=state.tree.model_dump()
    )

    pdf_path = await cv_renderer.render_pdf(
        rendered_html,
        temp=True
    )

    return pdf_path


# ==========================================================
# ROUTES
# ==========================================================

@app.get("/")
def home():
    return {
        "response": "welcome home"
    }


@app.post("/query")
def llm_query(data: Query):

    response = model.invoke([
        SystemMessage(
            content="You are a helpful assistant"
        ),
        HumanMessage(
            content=data.request
        )
    ])

    return {
        "response": response.content
    }


@app.post("/upload")
async def upload(
    file: UploadFile = File(...)
):

    extracted_content = await aextract_file(file)

    state.upload = extracted_content

    return {
        "status": "ok",
        "message": "CV uploaded successfully"
    }


@app.post("/execute")
async def execute(
    data: TemplateRequest
):

    if not state.upload:
        raise HTTPException(
            status_code=400,
            detail="Upload a CV first."
        )

    state.template = TemplateSelection(
        slot=data.slot,
        variant=data.variant
    )
    


    state.analysis = analyze_cv(
        state.upload
    )

    state.cv_ir = write_cv(
        state.upload,
        state.analysis
    )

    state.tree = tree_builder.build(
        state.cv_ir
    )

    pdf_path = await render_current_template()

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename="cv_server.pdf"
    )


@app.post("/display")
async def display(
    data: TemplateRequest
):

    if state.tree is None:
        raise HTTPException(
            status_code=400,
            detail="Generate a CV first."
        )

    state.template = TemplateSelection(
        slot=data.slot,
        variant=data.variant
    )

    pdf_path = await render_current_template()

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename="cv_server.pdf"
    )