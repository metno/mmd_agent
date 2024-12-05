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
import time
import xml.etree.ElementTree as ET
import re


# Read environment variable, INFO if variable is not set
log_level = os.environ.get("UNSENT-MMD-HANDLER_LOGLEVEL", "INFO")
api_key = os.environ.get('API_KEY')

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
def send_to_dmci(mmd, dmci_url):

    url = dmci_url + '/v1/insert'
    headers = {
        "apikey": api_key
    }
    response = requests.post(url,headers=headers ,data=mmd)

    if response.status_code == 503:
        raise requests.exceptions.RequestException(
            f"API returned {response.status_code} status code")

    return response.status_code, response.text


def main(mmd_path, dmci_url):

    try:
        with open(mmd_path, "r") as xml_file:
            incoming_mmd = xml_file.read()

        # Parse the XML content
        root = ET.fromstring(incoming_mmd)
        filename_xml = ''
        # Find the file_name element
        file_name_element = root.find(".//mmd:file_name",
                                      namespaces={'mmd': 'http://www.met.no/schema/mmd'})

        if file_name_element is not None:
            filename = file_name_element.text
            filename_xml = filename.replace(".nc", ".xml")

        mmd = incoming_mmd.encode()
        status_code, msg = send_to_dmci(mmd, dmci_url)

        if status_code == 200:
            logger.info("MMD file %s was successfully ingested with DMCI.", filename_xml)
        else:
            logger.error("Failed to push MMD file %s to DMCI. Status code : %s ",
                         filename_xml, status_code)

            # Extracting the line beginning with required string:
            first_line_match = re.search(r'^.*$', msg, re.MULTILINE)
            first_line = first_line_match.group(0) if first_line_match else None

            file_line_match = re.search(r'^- file::.*$', msg, re.MULTILINE)
            file_line = file_line_match.group(0) if file_line_match else None

            detail_line_match = re.search(r'^DETAIL:.*$', msg, re.MULTILINE)
            detail_line = detail_line_match.group(0) if detail_line_match else None

            solr_line_match = re.search(r'^ - solr:.*$', msg, re.MULTILINE)
            solr_line = solr_line_match.group(0) if solr_line_match else None

            error_lines = []

            if first_line:
                error_lines.append(f'{first_line}')

            if file_line:
                error_lines.append(f'{file_line}')

            if detail_line:
                error_lines.append(f'{detail_line}')

            if solr_line:
                error_lines.append(f'{solr_line}')

            if not any([first_line, file_line, detail_line, solr_line]):
                logger.error(f'{msg}')
            else:
                logger.error('\n'.join(error_lines))

        os.remove(mmd_path)
        logger.info("Removed the file from unsent_mmd directory.")

    except Exception as e:
        logger.error(f"Failed to sent. {e}")


if __name__ == "__main__":  # pragma: no cover

    dmci_url, unsent_mmd_path = read_config()

    try:
        while True:
            if os.path.exists(unsent_mmd_path):
                for filename in os.listdir(unsent_mmd_path):
                    mmd_path = os.path.join(unsent_mmd_path, filename)
                    if os.path.isfile(mmd_path):
                        main(mmd_path, dmci_url)
            logger.info("Sleeping for 30 minutes.")
            time.sleep(1800)  # Sleep for 30 minutes before checking again
    except Exception as e:
        logger.error(f"Failed to sent. {e}")
