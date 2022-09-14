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

from mmd_agent.agent import send_to_dmci, validate_mmd

@pytest.mark.mmd_agent
def testMMDAgentAgentValidate_mmd(monkeypatch):
    class mockResp:
        text = "Mock Respone"
        status_code = 200

    with monkeypatch.context() as mp:
        mp.setattr(requests, "post", lambda *a,**k: mockResp)
        assert validate_mmd("") is True



"""
class TestScript(unittest.TestCase):


    def test_incoming_mmd_is_not_valid(self):
        self.assertFalse(validate_mmd("asdfA1qw"))


    @patch('script.requests')
    def test_validate_mmd_succes(self,mock_requests):

        mock_response=MagicMock()
        mock_response.status_code=200
        mock_response.text="Everything is OK"
        mock_requests.post.return_value=mock_response
        self.assertEqual(validate_mmd("mms"),True)

    @patch('script.requests')
    def test_validate_mmd_fails(self,mock_requests):

        mock_response=MagicMock(status_code=500)
        mock_response.text="Invalid mmd"
        mock_requests.post.return_value=mock_response
        self.assertEqual(validate_mmd("mms"),False)

    @patch('script.requests')
    def test_send_to_dmci_succes(self,mock_requests):

        mock_response=MagicMock()
        mock_response.status_code=200
        mock_response.text="Everything is OK"
        mock_requests.post.return_value=mock_response
        self.assertEqual(send_to_dmci("mms"),200)

    @patch('script.requests')
    def test_send_to_dmci_fails(self,mock_requests):

        mock_response=MagicMock(status_code=500)
        mock_response.text="Invalid mmd"
        mock_requests.post.return_value=mock_response
        self.assertEqual(send_to_dmci("mms"),500)

if __name__=='__script__':
    unittest.script()
"""