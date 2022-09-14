#!/usr/bin/env python3
import os
import requests

    
incoming_mmd=os.environ.get("MMS_PRODUCT_EVENT_MMD",None)


def validate_mmd(mmd):
    url='https://dmci-staging.s-enda.k8s.met.no/v1/validate'
    response = requests.post(url,data=mmd)
    return response.status_code==200

def send_to_dmci(mmd):
    print("Sending to dmci ")
    response = requests.post('https://dmci-staging.s-enda.k8s.met.no/v1/insert',data=mmd)
    return response.status_code

if incoming_mmd is not None and incoming_mmd !="" :
    mmd=incoming_mmd.encode()
    if validate_mmd(mmd):
        send_to_dmci(mmd)
    else:
        print("invalid mmd")
else :
    print("product event mmd is none or empty  ")