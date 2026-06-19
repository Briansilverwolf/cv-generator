from langchain_core.messages import SystemMessage, HumanMessage
from schema.cv import CVGenerationIR
from schema.ats import CVAnalysisIR
from llm import model


def write_cv(original:str, analysis:CVAnalysisIR)->CVGenerationIR:
    cv_model = model.with_structured_output(CVGenerationIR)

    response = cv_model.invoke([
        SystemMessage(
            content = "You are a professional in cv writting i want to recraft it to standard and professionalism, cv should be about 2 pages not more"
        ),
        HumanMessage(
            content= f"""
            Here is the original cv
            {original}
            
            Here is the analysis made from the above cv
            {analysis}
            
            craft the final cv
            """
            
        )
    ])
   
    return response