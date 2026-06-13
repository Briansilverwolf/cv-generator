from langchain_openai import ChatOpenAI
from config import Settings

settings = Settings()


model = ChatOpenAI(
    model=settings.model,
    api_key=settings.openai_api_key,
    base_url=settings.base_url,
    temperature=float(settings.temperature),
)



