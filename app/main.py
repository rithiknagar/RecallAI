from fastapi import FastAPI
from app.api.router import router

app=FastAPI()

@app.get("/")
def root():
    return{"message":"Application started successfully"}

app.include_router(router)