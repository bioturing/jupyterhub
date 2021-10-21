#!/usr/bin/env python3

import os
import requests

from typing import Optional
from fastapi import FastAPI, HTTPException
from urllib.request import urlretrieve


token = os.environ.get("NOTEBOOKREPO_API_TOKEN", None)
nb_apiserver = os.environ.get("NOTEBOOKREPO_SERVER", None)

app = FastAPI()

assert (token and nb_apiserver)

def provision(resource):
	# get the notebook file, bundle , or something else in the feature
	# TODO: add some naming method based on timestamp
	filepath = os.path.join(os.environ["HOME"], resource["filename"])
	nbfile, headers = urlretrieve(resource["download_link"], filepath)
	if not os.path.exists(nbfile):
		### Log, raise exception
		print(f"Cannot provision notebook: {filepath}")
		return None
	# update the environment

	filename = resource["filename"] 
	return f"/notebooks/{filename}"	

@app.post("/jupyterhub/user/{useremail}/nbapi/provision")
def nb_provision(nb_id: int):
	data = {"resource_type": "notebook", "id": nb_id, "token": "mytoken"}
	r = requests.post(url = f"{nb_apiserver}/get_notebooks/", params= data)
	if r.status_code != 200:
		raise HTTPException(status_code = r.status_code, detail = "Cannot get resource from notebook api server")
	else:
		resource = r.json()
		# TODO: add more sophisticate steps here for file ext
		nbfile = provision(resource)
		if not nbfile: # provision failed
			raise HTTPException(status_code = 502, detail = "Got the resource but failed to provision")
	return {"route": f"{nbfile}"}
			

