from fastapi import FastAPI
from pydantic import BaseModel
from renderer import render_template

app = FastAPI()

class PosterData(BaseModel):
    template: str
    data: dict

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/generate")
def generate(poster: PosterData):
    path = render_template(poster.template, poster.data)
    return {"image": path}
