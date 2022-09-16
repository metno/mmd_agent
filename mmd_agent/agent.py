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


def validate_mmd(mmd):
    url = 'https://dmci-dev.s-enda.k8s.met.no/v1/validate'
    response = requests.post(url, data=mmd)
    return response.status_code == 200


def send_to_dmci(mmd):
    print("Sending to dmci...")
    response = requests.post(
        'https://dmci-dev.s-enda.k8s.met.no/v1/insert', data=mmd
        )
    return response.status_code


def main(incoming_mmd):
    if incoming_mmd is not None and incoming_mmd != "":
        mmd = incoming_mmd.encode()
        if validate_mmd(mmd):
            if send_to_dmci(mmd) == 200:
                print("Succesfully saved")
            else:
                print("Failed to save")
                
        else:
            print("Invalid mmd")
    else:
        print("product event mmd is none or empty")


if __name__ == "__main__":  # pragma: no cover
    incoming_mmd = os.environ.get("MMS_PRODUCT_EVENT_MMD", None)
    main(incoming_mmd)
