import unittest
from unittest.mock import MagicMock, patch
from script import send_to_dmci,validate_mmd

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
