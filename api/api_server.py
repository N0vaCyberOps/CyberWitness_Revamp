from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API działa poprawnie"}

def run_api_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)
