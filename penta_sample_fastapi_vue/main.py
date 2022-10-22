import os
import shutil
from io import BytesIO

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.params import File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.templating import Jinja2Templates

PATH_UPLOAD_FOLDER = "./upload"
PATH_OUTPUT_FOLDER = "./output"
PATH_INPUT_IMAGE = os.path.join(PATH_UPLOAD_FOLDER, "input.png")
PATH_OUTPUT_IMAGE = os.path.join(PATH_OUTPUT_FOLDER, "output.png")


app = FastAPI(title="さぷりぺんたんの被写体検出", description="被写体を抽出するよ", version="1.0")

import mimetypes

mimetypes.init()
mimetypes.add_type("application/javascript", ".js")

#: Configure CORS
origins = ["http://localhost:8080", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="./templates/static"), name="static")
templates = Jinja2Templates(directory="./templates/")


@app.get("/")
def index(request: Request):
    if os.path.exists(PATH_UPLOAD_FOLDER):
        shutil.rmtree(PATH_UPLOAD_FOLDER)
    os.makedirs(PATH_UPLOAD_FOLDER)
    if os.path.exists(PATH_OUTPUT_FOLDER):
        shutil.rmtree(PATH_OUTPUT_FOLDER)
    os.makedirs(PATH_OUTPUT_FOLDER)
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def index(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(BytesIO(contents)).convert("RGB")
    input_image.save(PATH_INPUT_IMAGE)
    output_image = input_image.convert("L")
    output_image.save(PATH_OUTPUT_IMAGE)
    response = FileResponse(path=PATH_OUTPUT_IMAGE, filename="output.png")
    return response


if __name__ == "__main__":
    uvicorn.main(app=app)
