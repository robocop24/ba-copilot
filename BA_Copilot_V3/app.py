from fastapi import FastAPI
from pydantic import BaseModel


class GenerateRequest(BaseModel):
    requirement:str

app = FastAPI()

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.post("/generate")
def generate(request:GenerateRequest):
    return {
        "status":"success",
        "trace_id":"...",
        "report_path":"..."
        }