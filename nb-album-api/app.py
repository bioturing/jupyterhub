import os
import json

from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "https://jupyter-dev.bioturing.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hostname = os.environ.get("API_HOSTNAME", "http://127.0.0.1:8001")
data_dir = "/app/notebooks" 

# TODO: add database to store notebook here
albums = json.load(open(f"{data_dir}/notebook-index.json"))

@app.get("/")
def read_root():
    return albums

@app.get("/download/{filename:path}")
def download_notebook(filename: str):
    # TODO: check API token here
    filepath = os.path.join(data_dir, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/get_notebooks/")
def get_item(resource_type: str, id: int, token: str, request: Request):
    # TODO check api token
    filename = albums[id]["filename"]
    env_filename = albums[id]["env_filename"]
    return {
        "nb_download_link": f"{hostname}/download/{filename}",
        "env_download_link": f"{hostname}/download/{env_filename}", 
    }

