from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key :str
    model:str
    base_url:str
    temperature:str
    
    model_config  = SettingsConfigDict(
        env_file = ".env"
    ) 