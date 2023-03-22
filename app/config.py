
from pydantic import BaseModel, BaseSettings

DEFAULT_OPENAI_MODEL = 'gpt-3.5-turbo-0301'


class OpenAI(BaseModel):
    api_key: str = None
    model: str = DEFAULT_OPENAI_MODEL


class Server(BaseModel):
    debug: bool = False
    host: str = None
    port: int = 18080


class Settings(BaseSettings):
    openai: OpenAI = OpenAI()
    server: Server = Server()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '.'


settings = Settings()

if __name__ == '__main__':
    print(settings.dict())
