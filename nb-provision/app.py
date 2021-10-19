#!/usr/bin/env python3

import os
import requests
import json
from urllib.request import urlretrieve

API_TOKEN = os.environ.get(["API_TOKEN"], None)
NOTEBOOK_ID = os.environ.get(["NOTEBOOK_ID"], None)
RESOURCE_URL = os.environ.get(["RESOURCE_URL"], None)
HOME_VOLUME = os.environ.get(["HOME_VOLUME"], None)

assert (API_TOKEN and NOTEBOOK_ID and RESOURCE_URL and HOME_VOLUME)

def get_resource():
        data = {
                "resource_type" : "notebook",
                "id" : NOTEBOOK_ID,
                "token" : API_TOKEN
        }
        r = requests.post(RESOURCE_URL, data)
        if r.status_code == 200:
                return json.loads(r.text)
        raise Exception("Get resource status %s" % str(r))

def main():
        payload = get_resource()
        nb_file, headers = urlretrieve(payload["download_link"], payload["filename"])
        if os.path.exists(nb_file):
                print("Notebook provisioned successfully")
                return 0
        else:
                raise Exception("Notebook file doesn't exists after downloading")

if __name__ == "__main__":
        main()