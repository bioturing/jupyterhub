import os

from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

hostname = os.environ.get("API_HOSTNAME", "http://127.0.0.1:8001")
data_dir = os.environ.get("DATA_DIR", "./notebook-repo")

# TODO: add database to store notebook here
albums = [
    {
        "category": "RNA-Velocity",
        "name": "DentateGyrus",
        "filename": "velocyto/DentateGyrus.ipynb",
        "id": 1,
        "format": "IPython",
        "env_filename": "velocyto/environment.yaml",
    },	
]
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

