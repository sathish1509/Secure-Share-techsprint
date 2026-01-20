import requests
from django.conf import settings

def get_coursera_access_token():
    """
    Get an access token from Coursera's OAuth2 API using client credentials flow.
    
    Returns:
        dict: The JSON response containing the access token and other details,
              or None if there was an error
    """
    token_url = settings.COURSERA_API['TOKEN_URL']
    client_id = settings.COURSERA_API['CLIENT_ID']
    client_secret = settings.COURSERA_API['CLIENT_SECRET']
    
    print(f"Attempting to get access token from: {token_url}")
    
    # Set up the request data
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        # Make the POST request to get the access token
        response = requests.post(token_url, data=data, headers=headers)
        
        # Print response details for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        if response.status_code != 200:
            print(f"Error response body: {response.text}")
        
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting access token from Coursera: {e}")
        return None

def get_coursera_courses(access_token=None, limit=10, start=0):
    """
    Get a list of courses from Coursera's API.
    
    Args:
        access_token (str, optional): The OAuth2 access token. If not provided,
                                   a new token will be requested.
        limit (int): Number of courses to retrieve (default: 10)
        start (int): Starting index for pagination (default: 0)
        
    Returns:
        dict: The JSON response containing the list of courses,
              or None if there was an error
    """
    if not access_token:
        token_data = get_coursera_access_token()
        if not token_data or 'access_token' not in token_data:
            return None
        access_token = token_data['access_token']
    
    api_url = settings.COURSERA_API['COURSES_URL']
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'limit': limit,
        'start': start
    }
    
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting courses from Coursera: {e}")
        return None
