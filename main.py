from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from renderer import render_template
import os

app = FastAPI()

# sprístupní statické súbory (napr. output.png)

app.mount("/", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
with open("ui/index.html", encoding="utf-8") as f:
return f.read()

@app.post("/generate-form", response_class=HTMLResponse)
def generate_form(
title: str = Form(...),
body: str = Form(...),
date: str = Form(...),
signatures: str = Form(...)
):
try:
data = {
"title": title,
"body": body,
"date": date,
"signatures": [s.strip() for s in signatures.split(",") if s.strip()]
}

    path = render_template("official_notice", data)

    # cache busting (?t=...) aby sa obrázok vždy obnovil
    return f'<img src="/{path}?t={os.urandom(4).hex()}" style="max-width:100%;">'

except Exception as e:
    return f"<pre>Error: {str(e)}</pre>"

