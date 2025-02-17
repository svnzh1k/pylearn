from fastapi import FastAPI
from db.database import create_db_and_tables
from routes import auth

app = FastAPI()
create_db_and_tables()


app.include_router(auth.auth_router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
