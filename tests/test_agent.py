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
from mmd_agent.agent import send_to_dmci, validate_mmd, main


@pytest.mark.mmd_agent
def test_validate_mmd_if_incoming_mmd_is_valid(monkeypatch):
    class mockResp:
        text = "Mock Respone"
        status_code = 200

    with monkeypatch.context() as mp:
        mp.setattr(requests, "post", lambda *a, **k: mockResp)
        assert validate_mmd("") is True


@pytest.mark.mmd_agent
def test_send_to_dmci_if_mmd_is_successfully_sent(monkeypatch):
    class mockResp:
        text = "Mock Respone"
        status_code = 200
    with monkeypatch.context() as mp:
        mp.setattr(requests, "post", lambda *a, **k: mockResp)
        assert send_to_dmci("") == 200


@pytest.mark.mmd_agent
def test_main_if_incoming_mmd_is_empty(capfd):
    main("")
    out, err = capfd.readouterr()
    assert out == "product event mmd is none or empty\n"


@pytest.mark.mmd_agent
def test_main_if_incoming_mmd_is_none(capfd):
    main(None)
    out, err = capfd.readouterr()
    assert out == "product event mmd is none or empty\n"


@pytest.mark.mmd_agent
def test_main_if_mmd_is_valid_and_succesfully_sent(capfd, mocker):
    mocker.patch('mmd_agent.agent.validate_mmd', return_value=True)
    mocker.patch('mmd_agent.agent.send_to_dmci', return_value=200)
    main("mms")
    out, err = capfd.readouterr()
    assert out == "Succesfully saved\n"


@pytest.mark.mmd_agent
def test_main_if_mmd_is_not_valid(capfd, mocker):
    mocker.patch('mmd_agent.agent.validate_mmd', return_value=False)
    main("mms")
    out, err = capfd.readouterr()
    assert out == "Invalid mmd\n"


@pytest.mark.mmd_agent
def test_main_if_mmd_is_valid_and_failed_to_sent(capfd, mocker):
    mocker.patch('mmd_agent.agent.validate_mmd', return_value=True)
    mocker.patch('mmd_agent.agent.send_to_dmci', return_value=400)
    main("mms")
    out, err = capfd.readouterr()
    assert out == "Failed to save\n"
