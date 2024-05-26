import unittest
from unittest.mock import patch, MagicMock
from email_handler.fetch_email import UserEmailService, fetch_service_object
from googleapiclient.errors import HttpError

class TestUserEmailService(unittest.TestCase):

    @patch('email_handler.fetch_email.fetch_service_object')
    def test_get_user_email_success(self, mock_fetch_service_object):
        mock_service = MagicMock()
        mock_fetch_service_object.return_value = mock_service

        mock_get_profile = mock_service.users.return_value.getProfile.return_value
        mock_get_profile.execute.return_value = {'emailAddress': 'test@example.com'}
        
        user_email_service = UserEmailService()
        
        user_email_service.get_user_email()
        
        self.assertEqual(user_email_service.user_email, 'test@example.com')
        mock_fetch_service_object.assert_called_once()
        mock_service.users.assert_called_once_with()

    @patch('email_handler.fetch_email.fetch_service_object')
    def test_get_user_email_http_error(self, mock_fetch_service_object):
        mock_service = MagicMock()
        mock_fetch_service_object.return_value = mock_service

        mock_get_profile = mock_service.users.return_value.getProfile.return_value
        mock_get_profile.execute.side_effect = HttpError(
            resp=MagicMock(status=404),
            content=b'Not Found'
        )
        
        user_email_service = UserEmailService()
        
        with self.assertRaises(HttpError):
            user_email_service.get_user_email()
        
        mock_fetch_service_object.assert_called_once()
        mock_service.users.assert_called_once_with()

    def test_header_found(self):
        headers = [{"name": "name", "value": "Mohit Kumar"}, {"name": "idea", "value": "project"}]
        fetch_header_name = "name"
        result = UserEmailService().process_email_headers(headers, fetch_header_name)
        self.assertEqual(result, "Mohit Kumar")

    def test_header_not_found(self):
        headers = [{"name": "idea", "value": "project"}]
        fetch_header_name = "name"
        result = UserEmailService().process_email_headers(headers, fetch_header_name)
        self.assertIsNone(result)

    def test_empty_headers(self):
        headers = []
        fetch_header_name = "name"
        result = UserEmailService().process_email_headers(headers, fetch_header_name)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
