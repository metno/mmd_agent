"""
MMD_AGENT : Main Config
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
import yaml
import sys
import logging

logger = logging.getLogger(__name__)


# Read the config file and get the required data
def read_config(configFile=None):

    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if configFile is None:
        configFile = os.path.join(pkg_root, "config.yaml")
    if not os.path.isfile(configFile):
        logger.error("Config file not found: %s", configFile)
        sys.exit(1)
    else:
        try:
            with open(configFile, mode="r", encoding="utf8") as inFile:
                raw_conf = yaml.safe_load(inFile)
                dmci_url = raw_conf.get("dmci_url")
                unsent_file_path = raw_conf.get("unsent_file_path")
            if dmci_url is None or dmci_url == "":
                logger.error("Parameter dmci_url in config is not set")
                sys.exit(1)
            elif unsent_file_path is None or unsent_file_path == "":
                logger.error("Parameter unsent_file_path in config is not set")
                sys.exit(1)
            else:
                unsent_file_path = os.path.join(pkg_root, unsent_file_path)
                return dmci_url, unsent_file_path
        except Exception:
            logger.exception("Could not read file: %s", configFile)
            sys.exit(1)
