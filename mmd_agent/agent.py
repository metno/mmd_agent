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
import uuid
import re


# Read environment variable, INFO if variable is not set
log_level = os.environ.get("MMD_AGENT_LOGLEVEL", "INFO")

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


# Managing and saving unsent data as xml into a directory
def persist_unsent_mmd(data, unsent_mmd_path):

    # Cache the job file
    file_uuid = uuid.uuid4()
    full_path = os.path.join(
        unsent_mmd_path, f"{file_uuid}.xml")

    """Write the persistent file."""
    try:
        with open(full_path, "w") as queuefile:
            queuefile.write(data)
        return 200, "Saved in unsent_mmd directory."

    except Exception as e:
        logger.error(str(e))
        return 507, "Cannot write xml data to cache file."


# Send the mmd file to the dmci
def send_to_dmci(mmd, dmci_url):

    url = dmci_url + '/v1/insert'
    response = requests.post(url, data=mmd)
    # Check if the API call was successful
    if response.status_code == 503:
        raise requests.exceptions.RequestException(f"API returned {response.status_code}\
                                                   status code")
    return response.status_code, response.text


def main(incoming_mmd, product_location):

    # Check whether mmd is empty or not
    if incoming_mmd is not None and incoming_mmd != "":

        filename_xml = ""
        if product_location is not None and product_location != "":
            filename = os.path.basename(product_location)
            filename_xml = filename.replace(".nc", ".xml")

        mmd = incoming_mmd.encode()
        dmci_url, unsent_mmd_path = read_config()
        try:

            status_code, msg = send_to_dmci(mmd, dmci_url)
            if status_code == 200:
                logger.info("MMD file %s was successfully ingested with DMCI.", filename_xml)
            else:
                logger.error("Failed to push MMD file %s to DMCI. Status code : %s ",
                             filename_xml, status_code)
                error_lines = []
                if status_code == 500:

                    # Improving logs
                    # Extracting the first line
                    first_line_match = re.search(r'^.*$', msg, re.MULTILINE)
                    first_line = first_line_match.group(0) if first_line_match else None

                    # Extracting the line beginning with - file:
                    file_line_match = re.search(r'^- file::.*$', msg, re.MULTILINE)
                    file_line = file_line_match.group(0) if file_line_match else None
                    # Extracting the line beginning with DETAIL
                    detail_line_match = re.search(r'^DETAIL:.*$', msg, re.MULTILINE)
                    detail_line = detail_line_match.group(0) if detail_line_match else None

                    solr_line_match = re.search(r'^ - solr:.*$', msg, re.MULTILINE)
                    solr_line = solr_line_match.group(0) if solr_line_match else None

                    if first_line:
                        error_lines.append(f'{first_line}')

                    if file_line:
                        error_lines.append(f'{file_line}')

                    if detail_line:
                        error_lines.append(f'{detail_line}')

                    if solr_line:
                        error_lines.append(f'{solr_line}')

                if len(error_lines) > 0:
                    logger.error('\n'.join(error_lines))
                else:
                    logger.error(f'{msg}')

        except Exception as e:

            logger.error(f"Failed to send.{e}")
            logger.info("Moving file to unsent_mmd directory.")
            status_code, msg = persist_unsent_mmd(incoming_mmd, unsent_mmd_path)
            if status_code == 200:
                logger.info('{},{}'.format(status_code, msg))
            else:
                logger.error('{},{}'.format(status_code, msg))
    else:

        logger.warning("Given mmd is none or empty.")


if __name__ == "__main__":  # pragma: no cover

    # Read environment variable
    incoming_mmd = os.environ.get("MMS_PRODUCT_EVENT_MMD", None)
    product_location = os.environ.get("MMS_PRODUCT_EVENT_PRODUCT_LOCATION", None)

    main(incoming_mmd, product_location)
