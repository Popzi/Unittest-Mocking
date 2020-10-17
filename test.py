import unittest
from io import StringIO
from main import size_of,google_query
from requests.exceptions import HTTPError
import requests

try:
    from unittest import mock
except ImportError:
    import mock

class MockingTests(unittest.TestCase):
    # create / read file mock
    def test_fileCreate(self):
        with mock.patch('main.open') as mock_open:
            mock_open.return_value.__enter__.return_value = StringIO('mockingISfun')
            self.assertEqual(size_of(), 12)
    # load a website mocking
    def _mock_response(
        self,
        status=200,
        content="CONTENT",
        json_data=None,
        raise_for_status=None):

        mock_resp = mock.Mock()
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        mock_resp.status_code = status
        mock_resp.content = content
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp

    @mock.patch('requests.get')
    def test_google_query(self, mock_get):
        mock_resp = self._mock_response(content="MockingIsFun")
        mock_get.return_value = mock_resp

        result = google_query('mockingisfun')
        self.assertEqual(result, 'MockingIsFun')
        self.assertTrue(mock_resp.raise_for_status.called)

    @mock.patch('requests.get')
    def test_failed_query(self, mock_get):
        mock_resp = self._mock_response(status=500, raise_for_status=HTTPError("google is down"))
        mock_get.return_value = mock_resp
        self.assertRaises(HTTPError, google_query, 'mockingisfun')

class UnitTests(unittest.TestCase):
       # create / read file mock
    def test_fileCreate(self):
        self.assertEqual(size_of(), 12)
        

    def test_google_query(self):
        result = google_query('mockingisfun')
        self.assertTrue(result.startswith(b'<!doctype html>'))
        self.assertIn(b'value="mockingisfun"', result)
        self.assertTrue(result.endswith(b'</html>'))
  
if __name__ == '__main__':
    unittest.main()                                     