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
import logging
from config import read_config
from retry import retry
import time


# Read environment variable, INFO if variable is not set
log_level = os.environ.get("UNSENT-MMD-HANDLER_LOGLEVEL", "INFO")

# Create stream handlers and set format
formatter = logging.Formatter('%(name)s:%(asctime)s:%(levelname)s:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(log_level)
stream_handler.setFormatter(formatter)

# Setting logging level and handlers
logging.basicConfig(
    level=log_level,
    handlers=[stream_handler]
)
logger = logging.getLogger(__name__)


# Send the mmd file to the dmci
# Retry decorator reruns the method 'send_to_dmci' if an exception occurs.
@retry(requests.exceptions.RequestException, delay=4, tries=2, backoff=2)
def send_to_dmci(mmd, dmci_url):

    url = dmci_url + '/v1/insert'
    response = requests.post(url, data=mmd)

    if response.status_code == 503:
        raise requests.exceptions.RequestException(
            f"API returned {response.status_code} status code")

    return response.status_code, response.text


def main(mmd_path, dmci_url):

    try:
        with open(mmd_path, "r") as xml_file:
            incoming_mmd = xml_file.read()

        mmd = incoming_mmd.encode()
        status_code, msg = send_to_dmci(mmd, dmci_url)

        if status_code == 200:
            logger.info("Succesfully saved")
        else:
            logger.error("Failed to save")
            logger.error('{},{}'.format(status_code, msg))

        os.remove(mmd_path)
        logger.info("Removed the file from unsent_mmd directory")

    except Exception as e:
        logger.error(f"Failed to sent {e}")


if __name__ == "__main__":  # pragma: no cover

    dmci_url, unsent_mmd_path = read_config()

    try:
        while True:
            if os.path.exists(unsent_mmd_path):
                for filename in os.listdir(unsent_mmd_path):
                    mmd_path = os.path.join(unsent_mmd_path, filename)
                    if os.path.isfile(mmd_path):
                        main(mmd_path, dmci_url)
            time.sleep(10)  # Sleep for 10 seconds before checking again
            logger.info("Sleeping for 10 sec")
    except Exception as e:
        logger.error(f"Failed to sent {e}")
