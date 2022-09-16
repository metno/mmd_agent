#!/usr/bin/env python3

"""
MMD_AGENT : Main MMD agent
==================

Copyright 2021 MET Norway

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import requests
from config import read_config


def send_to_dmci(mmd):
    dmci_url = read_config()+'/v1/insert'
    response = requests.post(dmci_url, data=mmd)
    return response.status_code, response.text


def main(incoming_mmd):
    if incoming_mmd is not None and incoming_mmd != "":
        mmd = incoming_mmd.encode()
        status_code, msg = send_to_dmci(mmd)
        if status_code == 200:
            print("Succesfully saved")
        else:
            print("Failed to save")
            print(status_code, msg)
    else:
        print("Given mmd is none or empty")


if __name__ == "__main__":  # pragma: no cover
    incoming_mmd = os.environ.get("MMS_PRODUCT_EVENT_MMD", None)
    main(incoming_mmd)
