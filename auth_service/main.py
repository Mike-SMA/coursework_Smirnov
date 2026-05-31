from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.api.v1.router import router

app = FastAPI(title="Auth Service", version="1.0.0")
app.include_router(router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
