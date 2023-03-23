from pydantic import BaseModel, BaseSettings

DEFAULT_OPENAI_MODEL = "gpt-3.5-turbo-0301"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 18080


class OpenAI(BaseModel):
    api_key: str = None
    model: str = DEFAULT_OPENAI_MODEL


class Server(BaseModel):
    debug: bool = False
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT


class Settings(BaseSettings):
    openai: OpenAI = OpenAI()
    server: Server = Server()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


settings = Settings()

if __name__ == "__main__":
    print(settings.dict())
