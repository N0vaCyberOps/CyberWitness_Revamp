from fastapi import FastAPI
import uvicorn
import asyncio

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API działa poprawnie"}

async def run_api_server():
    """Uruchamia serwer FastAPI w asyncio"""
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()
