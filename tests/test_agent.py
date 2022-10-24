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
from mmd_agent.agent import send_to_dmci, main


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
        mp.setattr(mmd_agent.agent, "read_config", lambda *a: "url")
        mp.setattr(mmd_agent.agent, "send_to_dmci", lambda *a: (200, 'Succesfully saved'))
        main("mms")
        assert "Succesfully saved\n" in caplog.text


@pytest.mark.mmd_agent
def test_main_if_mmd_is_valid_and_failed_to_sent(caplog, monkeypatch):
    with monkeypatch.context() as mp:
        mp.setattr(mmd_agent.agent, "read_config", lambda *a: "url")
        mp.setattr(mmd_agent.agent, "send_to_dmci", lambda *a: (400, 'Failed to save'))
        main("mms")
        assert "Failed to save\n" in caplog.text
        assert "400,Failed to save\n" in caplog.text
