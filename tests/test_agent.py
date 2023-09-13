"""
MMD_AGENT : MMD Agent Test
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
from mmd_agent.agent import send_to_dmci, persist_unsent_mmd, main
from requests.exceptions import RequestException
from unittest.mock import patch


@pytest.mark.mmd_agent
def test_persist_unsent_mmd_succesfully(tmpdir, caplog):
    data = "testdata"
    unsent_mmd_path = tmpdir
    status_code, msg = persist_unsent_mmd(data, unsent_mmd_path)
    assert status_code == 200
    assert msg == "Saved in unsent_mmd directory"
    assert len(caplog.records) == 0


@pytest.mark.mmd_agent
def test_persist_unsent_mmd_failed(monkeypatch, caplog, tmpdir):

    directory_path = tmpdir
    data = "Test data"

    # Create a mock for the 'open' function that raises an exception
    with patch('builtins.open', side_effect=Exception('Test Exception')):
        status_code, msg = persist_unsent_mmd(data, directory_path)

    assert status_code == 507
    assert msg == "Cannot write xml data to cache file"

    assert len(caplog.records) == 1
    assert "Test Exception" in caplog.text


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
def test_main_if_incoming_mmd_is_empty(caplog):
    main("")
    assert "Given mmd is none or empty\n" in caplog.text


@pytest.mark.mmd_agent
def test_main_if_incoming_mmd_is_none(caplog):
    main(None)
    assert "Given mmd is none or empty\n" in caplog.text


@pytest.mark.mmd_agent
def test_main_if_mmd_is_succesfully_sent(caplog, monkeypatch):
    with monkeypatch.context() as mp:
        mp.setattr(mmd_agent.agent, "read_config", lambda *a: ("url", "unsent_mmd_path"))
        mp.setattr(mmd_agent.agent, "send_to_dmci", lambda *a: (200, 'Succesfully saved'))
        with caplog.at_level(logging.INFO):
            main("mms")
        assert "Succesfully saved\n" in caplog.text


@pytest.mark.mmd_agent
def test_main_if_mmd_is_valid_and_failed_to_save(caplog, monkeypatch):
    with monkeypatch.context() as mp:
        mp.setattr(mmd_agent.agent, "read_config", lambda *a: ("url", "unsent_mmd_path"))
        mp.setattr(mmd_agent.agent, "send_to_dmci", lambda *a: (400, 'Failed to save'))
        main("mms")
        assert "Failed to save\n" in caplog.text
        assert "400,Failed to save\n" in caplog.text


@pytest.mark.mmd_agent
def test_main_if_failed_to_sent_and_saved_to_unsent_mmd_directory(caplog, monkeypatch):

    with monkeypatch.context() as mp:
        mp.setattr(mmd_agent.agent, "read_config", lambda *a: ("url", "unsent_mmd_path"))
        mp.setattr(mmd_agent.agent, "persist_unsent_mmd",
                   lambda *a: (200, "Saved in unsent_mmd directory"))
        with pytest.raises(requests.exceptions.RequestException):
            send_to_dmci("mmd", "url")
        with caplog.at_level(logging.INFO):
            main("mms")
            assert "Failed to send." in caplog.text
            assert "Moving file to unsent_mmd directory\n" in caplog.text
            assert "200,Saved in unsent_mmd directory\n" in caplog.text


@pytest.mark.mmd_agent
def test_main_if_failed_to_sent_and_failed_to_save_to_unsent_mmd_directory(caplog, monkeypatch):

    with monkeypatch.context() as mp:
        mp.setattr(mmd_agent.agent, "read_config", lambda *a: ("url", "unsent_mmd_path"))
        mp.setattr(mmd_agent.agent, "persist_unsent_mmd",
                   lambda *a: (507, "Cannot write xml data to cache file"))
        # Raise an exception for send_to_dmci
        with pytest.raises(requests.exceptions.RequestException):
            send_to_dmci("mmd", "url")
        with caplog.at_level(logging.INFO):
            main("mms")
            assert "Failed to send." in caplog.text
            assert "Moving file to unsent_mmd directory\n" in caplog.text
            assert "507,Cannot write xml data to cache file\n" in caplog.text
