import app
import unittest
import requests
import html_to_json
import json

        
class Test_VenueAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = 'http://localhost:5000/'
        self.client = requests.Session()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.client.close()
        return super().tearDown()
    
    def test_get_all_venues(self):
        response = self.client.get(f'{self.base_url}/V2/venues')
        
        # Assert the response status code is OK
        self.assertEqual(response.status_code, 200)
        
        # Assert the response body or headers
        response_json = response.json
        
        response_json = html_to_json.convert(response.text)
        response_json_main = response_json["body"][0]["div"][0]["main"][0]
        
        self.assertTrue( "h3" in response_json_main, "The response does not contain any venue information. Perhaps the database is not loaded?" )