from fastapi import FastAPI
from mayim.extension import StarletteMayimExtension
from mayim import PostgresExecutor, query
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class EnvSettings(BaseSettings):
    db_dsn: str = "postgres"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = EnvSettings()


class Executor(PostgresExecutor):
    @query("""SELECT * FROM user""")
    async def get_test(self) -> dict:
        ...


app = FastAPI(
    docs_url="/"
)
dsn = settings.db_dsn
ext = StarletteMayimExtension(executors=[Executor], dsn=dsn)


@app.get("/query")
async def query():
    executor = Executor()
    return await executor.get_test()


ext.init_app(app)




