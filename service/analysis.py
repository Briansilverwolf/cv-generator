from langchain_core.messages import SystemMessage, HumanMessage
from schema.ats import CVAnalysisIR
from app.llm import model


def analyze_cv(cv_text:str)->CVAnalysisIR:
    cv_model = model.with_structured_output(CVAnalysisIR)
    response = cv_model.invoke([
        SystemMessage(
            content = "You are to analyze the following cv, on ats analysis should be out of 100"
        ),
        HumanMessage(
            content= cv_text
        )
    ])
    return response