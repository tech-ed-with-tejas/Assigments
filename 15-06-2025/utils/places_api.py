import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json
from langchain_core.tools import tool


API_KEY = os.getenv("PLACES_API_KEY") # Replace with your actual API Key
def get_lat_long_from_string(address_string):
    """
    Gets the latitude and longitude for a given address string using the Google Geocoding API.

    Args:
        address_string (str): The address or place name to geocode (e.g., "Eiffel Tower", "London", "1600 Amphitheatre Parkway, Mountain View, CA").

    Returns:
        tuple: A tuple (latitude, longitude) if successful, None otherwise.
    """
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address_string,
        "key": API_KEY
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data["status"] == "OK":
            # The API can return multiple results; we usually take the first one.
            # Check for results and geometry structure
            if data["results"]:
                location = data["results"][0]["geometry"]["location"]
                latitude = location["lat"]
                longitude = location["lng"]
                # print(f"Successfully geocoded '{address_string}': Lat={latitude}, Lng={longitude}")
                return latitude, longitude
            else:
                print(f"No results found for '{address_string}'.")
                return None
        elif data["status"] == "ZERO_RESULTS":
            print(f"No results found for '{address_string}'. Check the spelling or try a more specific address.")
            return None
        else:
            print(f"Geocoding API error for '{address_string}': {data['status']} - {data.get('error_message', 'No specific error message.')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error during geocoding: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing Geocoding API response for '{address_string}': Missing key {e}. Response: {data}")
        return None



def search_nearby_restaurants(latitude, longitude, radius, max_results=10):
    """
    Performs a Nearby Search for restaurants using the new Google Places API.

    Args:
        latitude (float): The latitude of the center of the search circle.
        longitude (float): The longitude of the center of the search circle.
        radius (float): The radius in meters to search within.
        max_results (int, optional): The maximum number of results to return (up to 20). Defaults to 10.

    Returns:
        dict: The JSON response from the Places API, or None if an error occurs.
    """
    url = "https://places.googleapis.com/v1/places:searchNearby"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        # Field mask from your curl command, requesting only displayName
        "X-Goog-FieldMask": "places.displayName" 
    }
    
    data = {
        "includedTypes": ["restaurant", "tourist_attraction", "museum", "park", "zoo", "art_gallery", "amusement_park", "aquarium", "historical_landmark"],
        "maxResultCount": max_results,
        "rankPreference":"POPULARITY",
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": radius,
                
            }
        }
    }
    try:
        # print(data)
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None


@tool
def get_famous_places_nearby(address, radius_km=10):
    """
    Gets a list of famous places near a given address and returns them as a joined string.

    Args:
        address (str): The address or place name to search nearby.
        radius_km (int, optional): The radius in kilometers to search within. Defaults to 10.

    Returns:
        str: A string listing the famous places nearby, or an error message if no places are found.
    """
    response = get_lat_long_from_string(address)
    if response is not None:
        results = search_nearby_restaurants(response[0], response[1], radius_km * 1000)
        places = [place.get("displayName", {}).get("text", "") for place in results.get("places", [])]
        if places:
            return f"The famous places include: {', '.join(places)}"
        else:
            return "No famous places found nearby."
    else:
        return "Could not retrieve location coordinates."

# Example usage
if __name__ == "__main__":
    print(get_famous_places_nearby("Bangalore, Karnataka, India"))
  