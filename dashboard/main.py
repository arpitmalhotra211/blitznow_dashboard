from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import shutil
import os

from analyzer import analyze_file

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_PATH = "uploaded_file"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from fastapi import UploadFile, File
import shutil
import os

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    import shutil

    if not file:
        return {"levels": {}, "error": "No file uploaded"}

    file_path = "uploaded.xlsx"  # force Excel only

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return {"levels": {}, "error": f"File save failed: {str(e)}"}

    return analyze_file(file_path)