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
    
    def test_get_all_venues_then_get_details_of_first(self):
        response_all = self.client.get(f'{self.base_url}/V2/venues')
        
        # Assert the response status code is OK
        self.assertEqual(response_all.status_code, 200, "Couldn't get any venues, is the database loaded?")
        
        # Assert the response body or headers
        response_json = response_all.json
        
        response_json = html_to_json.convert(response_all.text)
        first_venue_uri = response_json["body"][0]["div"][0]["main"][0]["ul"][0]["li"][0]["a"][0]["_attributes"]['href']
        
        response_venue = self.client.get(f'{self.base_url}{first_venue_uri}')
        
        self.assertEqual(response_venue.status_code, 200, "Couldn't retrieve the first venue.")
        
    
    def test_get_all_venues_gets_at_least_one_city(self):
        
        # Assert the response status code is OK
        self.assertEqual(response.status_code, 200)
        
        # Assert the response body or headers
        response_json = response.json
        
        response_json = html_to_json.convert(response.text)
        response_json_main = response_json["body"][0]["div"][0]["main"][0]
        
        self.assertTrue( "h3" in response_json_main, "The response does not contain any cities. Perhaps the database is not loaded?" )

    def test_get_all_venues_gets_at_least_one_venue(self):
        response = self.client.get(f'{self.base_url}/V2/venues')
        
        # Assert the response status code is OK
        self.assertEqual(response.status_code, 200)
        
        # Assert the response body or headers
        response_json = response.json
        
        response_json = html_to_json.convert(response.text)
        response_json_venue_list = response_json["body"][0]["div"][0]["main"][0]["ul"][0]
        
        self.assertTrue( "li" in response_json_venue_list, "The response does not contain any venue information within a city." )        
        

    def test_search_any_venue_finds_at_least_one(self):
        response = self.client.post(f'{self.base_url}/V2/venues/search',{"search_term": ""})
        
        print(response.text)
        # Assert the response status code is OK
        self.assertEqual(response.status_code, 200)

        # Assert the response body or headers      
        response_json = html_to_json.convert(response.text)
        response_json_venue_list = response_json["body"][0]["div"][0]["main"][0]["ul"][0]

        self.assertTrue( "li" in response_json_venue_list, "The search response does not contain any venue." )        
        
    # Assume that we can and will create an in-memory database double for testing against
    # the database double will be refreshed each time the test suite is run
    def test_post_then_find_a_venue(self):
        test_venue_data = {
            "name" : "test_venue_name",
            "city" : "test_venue_city",
            "state" : "test_venue_state",
            "address" : "test_venue_address",
            "phone" : "test_venue_phone",
            "genres" : "test_venue_genre1, test_venue_genre2",
            "facebook_link" : "test_venue_facebook_link",
            "image_link" : "test_venue_image_link",
            "website_link" : "test_venue_website_link",
            "seeking_talent" : "test_venue_seeking_talent",
            "seeking_talent_description" : "test_venue_seeking_talent_description"
        }
        
        self.client.post(f'{self.base_url}/V2/venues/create', test_venue_data)
        
        response = self.client.post(f'{self.base_url}/V2/venues/search',{"search_term": "test_venue_name"})
        
        # Assert the response status code is OK
        self.assertEqual(response.status_code, 200)

        # Assert the response body or headers      
        response_json = html_to_json.convert(response.text)
        response_json_venue_list = response_json["body"][0]["div"][0]["main"][0]["ul"][0]

        self.assertTrue( "li" in response_json_venue_list, "The venue could not be retrieved. Either it wasn't properly posted or the search did not work. This is a round trip test." )   
        
    def test_post_delete_a_venue(self):
        test_venue_data = {
            "name" : "test_venue_name_delete",
            "city" : "test_venue_city",
            "state" : "test_venue_state",
            "address" : "test_venue_address",
            "phone" : "test_venue_phone",
            "genres" : "test_venue_genre1, test_venue_genre2",
            "facebook_link" : "test_venue_facebook_link",
            "image_link" : "test_venue_image_link",
            "website_link" : "test_venue_website_link",
            "seeking_talent" : "test_venue_seeking_talent",
            "seeking_talent_description" : "test_venue_seeking_talent_description"
        }
        
        self.client.post(f'{self.base_url}/V2/venues/create', test_venue_data)
        
        response = self.client.post(f'{self.base_url}/V2/venues/search',{"search_term": "test_venue_name_delete"})
        
        # Assert the response status code is OK
        self.assertEqual(response.status_code, 200)

        # Assert the response body or headers      
        response_json = html_to_json.convert(response.text)
        response_json_venue_list = response_json["body"][0]["div"][0]["main"][0]["ul"][0]

        self.assertTrue( "li" in response_json_venue_list, "The venue could not be retrieved. Either it wasn't properly posted or the search did not work. This is a round trip test." )   
        response_json_venue_uri = response_json["body"][0]["div"][0]["main"][0]["ul"][0]["li"][0]["a"][0]["_attributes"]['href']
        print (response_json_venue_uri)
        delete_response = self.client.delete(f'{self.base_url}/V2/{response_json_venue_uri}')
        
        self.assertEqual( delete_response.status_code, 200 )