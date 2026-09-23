from collections.abc import Generator

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Configuracoes(BaseSettings):
    db_user: str | None = None
    db_password: str | None = None
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


configuracoes = Configuracoes()

# Prefer MySQL when all DB vars are set; otherwise fall back to a local SQLite file for dev.
if configuracoes.db_user and configuracoes.db_name:
    DATABASE_URL = (
        f"mysql+pymysql://{configuracoes.db_user}:{configuracoes.db_password}"
        f"@{configuracoes.db_host}:{configuracoes.db_port}/{configuracoes.db_name}"
    )
else:
    DATABASE_URL = "sqlite:///./biblioteca_dev.db"

mecanismo_banco = create_engine(DATABASE_URL, pool_pre_ping=True)
criar_sessao = sessionmaker(bind=mecanismo_banco, autoflush=False, autocommit=False)


class BaseBanco(DeclarativeBase):
    pass


def obter_sessao_banco() -> Generator[Session, None, None]:
    sessao_banco = criar_sessao()

    try:
        yield sessao_banco
    finally:
        sessao_banco.close()