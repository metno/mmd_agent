import os
import yaml


def read_config():
    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    configFile = os.path.join(pkg_root, "example_config.yaml")
    with open(configFile, mode="r", encoding="utf8") as inFile:
        raw_conf = yaml.safe_load(inFile)
    dmci_url = raw_conf.get("dmci_url")
    return dmci_url
