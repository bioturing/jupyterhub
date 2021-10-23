#!/usr/bin/env python3

import os
import requests
import tempfile
import sys
import uuid
import asyncio
import json

from loguru import logger
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket
from urllib.request import urlretrieve

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from prov_env import create_conda_env, install_kernelspec_python, patching_kernelname_ipynb, env_sha1_hashing
from orm import NBProvisionRecord, Base

token = os.environ.get("NOTEBOOKREPO_API_TOKEN", "notoken")
nb_apiserver = os.environ.get("NOTEBOOKREPO_SERVER", None)

logger.remove()
logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | APP-{level} | <level>{message}</level>")

assert (token and nb_apiserver)

dbfile = f"{os.environ['HOME']}/.nb-provision.db"
engine = create_engine(f'sqlite:///{dbfile}', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = FastAPI()

for prov in session.query(NBProvisionRecord).all():
    prov.progress = 100

session.commit()

# TODO: bring this to utils
def sanity_check(file, http_headers):
    headers_dict = dict(http_headers)
    # TODO: sha256 checksum here
    return os.stat(file).st_size == int(headers_dict["content-length"])

# TODO: Notebook as a class and provision as a function
def provision(resource, uid, useremail):

    # TODO: get the checksum of resource, then only provision one
    prov_orm = NBProvisionRecord(uid=str(uid), useremail=useremail, status="Initializing")
    session.add(prov_orm)
    session.commit()

    def log_update_orm(msg: str, prog : int = 0 ):
        # TODO: update all provisioning jobs that has the same checksum
        prov_orm.logmess = msg
        if prog:
            prov_orm.progress = prog
        session.commit()
        logger.warning(msg)

    # get the notebook file, bundle , or something else in the feature
    # TODO: add some naming method based on timestamp
    nb_filename = os.path.basename(resource["nb_download_link"])
    prov_orm.notebookname = nb_filename

    # TODO: check if notebook is exists, if yes, check the watermark to see if we need to update the new version
    nbfile = os.path.join(os.environ["HOME"], nb_filename)
    envfile = os.path.join(tempfile.mkdtemp(), "environment.yaml")

    log_update_orm(f"Downloading notebook...", 10)
    _, nb_headers = urlretrieve(resource["nb_download_link"], nbfile)
    _, env_headers = urlretrieve(resource["env_download_link"], envfile)

    if not sanity_check(nbfile, nb_headers) or not sanity_check(envfile, env_headers):
        prov_orm.status = "Failed" 
        log_update_orm(f"Sanity check failed. Cannot provision notebook: {nb_filename}")
        return

    # update the environment
    envname = nb_filename + env_sha1_hashing(envfile)[:8]
    prov_orm.envname = envname
    log_update_orm(f"Creating conda environment...", 30)
    if not create_conda_env(envfile, envname): # error
        prov_orm.status = "Failed" 
        log_update_orm(f"Cannot create conda environment {envname}", 100)
        return

    log_update_orm(f"Installing kernelspec...", 50)
    if not install_kernelspec_python(envname):
        prov_orm.status = "Failed" 
        log_update_orm(f"Cannot install kernelspec {envname}", 100)
        return

    log_update_orm(f"Patching kernel...", 60)
    if not patching_kernelname_ipynb(nbfile, envname):
        prov_orm.status = "Failed" 
        log_update_orm(f"Cannot patch kernel name for notebook {nb_filename}", 100)
        return
    prov_orm.status = "Success" 
    log_update_orm(f"Provision notebook {nb_filename} successfully", 100)

@app.get("/jupyterhub/user/{useremail}/nbapi/provision-pending/{uid}")
async def get_provision_status(uid: str):
    prov_orm = session.query(NBProvisionRecord).filter_by(uid=uid).all()
    if not prov_orm:
        raise HTTPException(status_code=404, detail = "Not found")
    return prov_orm[0].to_dict()

@app.websocket("/jupyterhub/user/{useremail}/nbapi/provision-pending/{uid}")
async def websocket_endpoint(
    websocket: WebSocket,
    uid: str,
    # cookie_or_token: str = Depends(get_cookie_or_token),
):
    await websocket.accept()
    logger.info(f"Connected: {uid}")

    while True:
        await asyncio.sleep(0.5)
        prov_orm = session.query(NBProvisionRecord).filter_by(uid=uid).all()
        if not prov_orm:
            await websocket.close()
            return
        elif prov_orm[0].progress == 100:
            await websocket.send_json(prov_orm[0].to_dict())
            await websocket.close()
            session.commit()
            return
        await websocket.send_json(prov_orm[0].to_dict())

@app.post("/jupyterhub/user/{useremail}/nbapi/provision", status_code = 202)
async def nb_provision(nb_id: int, useremail: str, background_tasks : BackgroundTasks):
    data = {"resource_type": "notebook", "id": nb_id, "token": "mytoken"}
    r = requests.post(url = f"{nb_apiserver}/get_notebooks/", params= data)
    if r.status_code != 200:
        raise HTTPException(status_code = r.status_code, detail = "Cannot get resource from notebook api server")
    else:
        resource = r.json()
        uid = uuid.uuid4()
        # TODO: add more sophisticate steps here for file ext
        background_tasks.add_task(provision, resource, uid, useremail) 
        return {"uuid": uid}

