"""
MMD_AGENT : MMD Agent handler Test
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

import pytest
import requests
import mmd_agent
import logging
from mmd_agent.handler import send_to_dmci, main
from requests.exceptions import RequestException


@pytest.mark.mmd_agent
def test_send_to_dmci_if_mmd_is_successfully_sent(monkeypatch):
    class mockResp:
        text = "Saved succesfully"
        status_code = 200
    with monkeypatch.context() as mp:
        mp.setattr(requests, "post", lambda *a, **k: mockResp)
        status_code, msg = send_to_dmci("mmd", "url")
        assert status_code == 200
        assert msg == "Saved succesfully"


@pytest.mark.mmd_agent
def test_send_to_dmci_raise_an_exception(monkeypatch):
    class mockResp:
        text = "Not saved succesfully"
        status_code = 503
    with monkeypatch.context() as mp:
        mp.setattr(requests, "post", lambda *a, **k: mockResp)
        with pytest.raises(RequestException):
            send_to_dmci("mmd", "url")


@pytest.mark.mmd_agent
def test_main_if_mmd_is_succesfully_sent_and_saved_archive(
        caplog, monkeypatch, tmpdir):

    xml_content = """<mmd:mmd xmlns:mmd="http://www.met.no/schema/mmd"
        xmlns:gml="http://www.opengis.net/gml">
        <mmd:metadata_identifier>avb</mmd:metadata_identifier>
        <mmd:storage_information>
        <mmd:file_name>reference_nc.nc</mmd:file_name>
        </mmd:storage_information>
    </mmd:mmd>
    """
    testFile = tmpdir.join("testfile.xml")
    testFile.write(xml_content)

    with monkeypatch.context() as mp:
        mp.setattr(mmd_agent.handler, "read_config", lambda *a:
                   ("url", "unsent_mmd_path"))
        mp.setattr(mmd_agent.handler, "send_to_dmci", lambda *a:
                   (200, 'Succesfully saved'))
        with caplog.at_level(logging.INFO):
            main(testFile, "dmci-url")
            assert "MMD file reference_nc.xml was successfully ingested with DMCI." in caplog.text
            assert "Removed the file from unsent_mmd directory" in caplog.text


@pytest.mark.mmd_agent
def test_main_if_mmd_is_succesfully_sent_and_saved_rejected(
        caplog, monkeypatch, tmpdir):

    xml_content = """<mmd:mmd xmlns:mmd="http://www.met.no/schema/mmd"
        xmlns:gml="http://www.opengis.net/gml">
        <mmd:metadata_identifier>avb</mmd:metadata_identifier>
        <mmd:storage_information>
        <mmd:file_name>reference_nc.nc</mmd:file_name>
        </mmd:storage_information>
    </mmd:mmd>
    """
    testFile = tmpdir.join("testfile.xml")
    testFile.write(xml_content)
    with monkeypatch.context() as mp:
        mp.setattr(mmd_agent.handler, "read_config", lambda *a:
                   ("url", "unsent_file_path"))
        mp.setattr(mmd_agent.handler, "send_to_dmci", lambda *a:
                   (400, 'Rejected'))
        with caplog.at_level(logging.INFO):
            main(testFile, "dmci-url")
            assert "Failed to push MMD file reference_nc.xml to DMCI." in caplog.text
            assert "Rejected" in caplog.text
            assert "Removed the file from unsent_mmd directory" in caplog.text


@pytest.mark.mmd_agent
def test_main_if_failed_to_sent(caplog, monkeypatch, tmpdir):

    xml_content = """<mmd:mmd xmlns:mmd="http://www.met.no/schema/mmd"
        xmlns:gml="http://www.opengis.net/gml">
        <mmd:metadata_identifier>avb</mmd:metadata_identifier>
        <mmd:storage_information>
        <mmd:file_name>reference_nc.nc</mmd:file_name>
        </mmd:storage_information>
    </mmd:mmd>
    """
    testFile = tmpdir.join("testfile.xml")
    testFile.write(xml_content)

    with pytest.raises(requests.exceptions.RequestException):
        send_to_dmci("mmd", "url")
    with caplog.at_level(logging.INFO):
        main(testFile, "url")
    assert "Failed to sent" in caplog.text
