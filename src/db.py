from sqlalchemy import create_engine, text 
from . import settings

def pg_engine():
    url = (
        f"postgresql+psycopg://{settings.PG_USER}:{settings.PG_PASS}"
        f"@{settings.PG_HOST}:{settings.PG_PORT}/{settings.PG_DB}"
    )
    return create_engine(url, pool_pre_ping=True)

def execute_sql(sql):
    eng = pg_engine()
    with eng.begin() as conn:
        conn.execute(text(sql))