import os

from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

hostname = os.environ.get("API_HOSTNAME", "http://127.0.0.1:8001")
data_dir = os.environ.get("DATA_DIR", "./notebooks")
albums = [
	{
		"category": "Cell-cell communication",
		"name": "Infere cell-cell communication using Cellchat",
		"filename": "CellChat-vignette.Rmd",
		"id": 0,
		"format": "Rmd",
	},
	{
		"category": "Cell Assigment",
		"name": "Annotation with CellAssign",
		"filename": "‘cellassign_tutorial.ipynb’",
		"id": 1,
		"format": "IPython"
	},	
]
@app.get("/")
def read_root():
    return albums

@app.get("/download/{filename}")
def download_notebook(filename: str):
	filepath = os.path.join(data_dir, filename)
	if os.path.exists(filepath):
		return FileResponse(filepath)
	else:
		raise HTTPException(status_code=404, detail="Item not found")

@app.post("/get_notebooks/")
def get_item(resource_type: str, id: int, token: str, request: Request):
	# check api token
	filename = albums[id]["filename"]
	return {
		"download_link": f"{hostname}/download/{filename}",
		"filename": filename
	}

