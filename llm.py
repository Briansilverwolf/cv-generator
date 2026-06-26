from langchain_openai import ChatOpenAI
from config import Settings

settings = Settings()


model = ChatOpenAI(
    model=settings.model,
    api_key=settings.openai_api_key,
    base_url=settings.base_url,
    temperature=float(settings.temperature),
)



print("API_KEY:", bool(settings.openai_api_key))
print("MODEL:", repr(settings.model))
print("BASE_URL:", repr(settings.base_url))
print("TEMPERATURE:", repr(settings.temperature))