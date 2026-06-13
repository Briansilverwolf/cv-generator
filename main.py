from langchain_core.messages import HumanMessage, SystemMessage
from fastapi import FastAPI, UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse 


from llm import model
from utils.extract import aextract_file
from service import analyze_cv, write_cv
from renders import CVRenderer
from state import CVState

state = CVState()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    request:str

@app.get("/")
def home():
    return{"response":"welcome home"}

@app.get("/query")
def llm_query(data:Query):
    response = model.invoke([
        SystemMessage(
            content = "You are a helpfull assistance"
        ),
        HumanMessage(
            content = data.request
        )
    ])
    return {"response":response.content}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    extracted_content = await aextract_file(file)
    state.upload = extracted_content
    return {
        "status":"ok"
    }


@app.post("/execute")
async def execute():
    state.analysis = analyze_cv(state.upload)
    state.cv_ir = write_cv(state.upload, state.analysis)
    
        
    tree_builder = RenderTreeBuilder()
    tree = tree_builder.build(state.cv_ir)
    engine_template = TemplateEngine("template")
    template = engine_template.render(
        template= TemplateSelection(
            slot="professional",
            variant="compact"
        ),
        render_tree=tree.model_dump()
    )
        
    
    
    return FileResponse(
        path = pdf,
        filename = "cv_server.pdf"
    )
    
s

