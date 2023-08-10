import unittest
import requests
import html_to_json

class Test_ShowAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = 'http://localhost:5000/'
        self.client = requests.Session()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.client.close()
        return super().tearDown()
    
    def test_shows_page_lists_at_least_one_show(self):
        response = self.client.get(f'{self.base_url}/V2/shows')
        
        # Assert the response status code is OK
        self.assertEqual(response.status_code, 200)
        
        # Assert the response body or headers
        
        response_json = html_to_json.convert(response.text)
        response_json_main = response_json["body"][0]["div"][0]["main"][0]["div"][0]
        
        self.assertTrue( "div" in response_json_main, "The response does not contain any Shows. Perhaps the database is not loaded?" )   