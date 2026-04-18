from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from renderer import render_template
import os

# vytvorenie aplikácie

app = FastAPI()

# statické súbory (obrázky ako output.png)

app.mount("/static", StaticFiles(directory="."), name="static")

# hlavná stránka (UI)

@app.get("/", response_class=HTMLResponse)
def index():
with open("ui/index.html", encoding="utf-8") as f:
return f.read()

# spracovanie formulára

@app.post("/generate-form", response_class=HTMLResponse)
def generate_form(
title: str = Form(...),
body: str = Form(...),
date: str = Form(...),
signatures: str = Form(...)
):
try:
# spracovanie dát z formulára
data = {
"title": title,
"body": body,
"date": date,
"signatures": [s.strip() for s in signatures.split(",") if s.strip()]
}


    # zavolanie renderera
    path = render_template("official_notice", data)

    # vrátenie obrázka (HTMX ho vloží do stránky)
    return f'<img src="/static/{path}?t={os.urandom(4).hex()}" style="max-width:100%;">'

except Exception as e:
    # zobrazí chybu priamo na stránke
    return f"<pre>Error: {str(e)}</pre>"

