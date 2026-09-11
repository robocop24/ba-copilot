from fastapi import FastAPI
from pydantic import BaseModel
from workflow import run_ba_workflow


class GenerateRequest(BaseModel):
    requirement:str

app = FastAPI()

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.post("/generate")
def generate(request:GenerateRequest):
    return run_ba_workflow(request.requirement, approve=lambda msg: True)