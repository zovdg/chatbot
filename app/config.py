
from pydantic import BaseModel, BaseSettings

DEFAULT_OPENAI_MODEL = 'gpt-3.5-turbo-0301'


class OpenAI(BaseModel):
    api_key: str = None
    model: str = DEFAULT_OPENAI_MODEL


class Settings(BaseSettings):
    openai: OpenAI = OpenAI()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '.'


settings = Settings()

if __name__ == '__main__':
    print(settings.dict())
