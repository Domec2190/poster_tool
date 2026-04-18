from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
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
    try:
        path = render_template(poster.template, poster.data)
        return FileResponse(path, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}
