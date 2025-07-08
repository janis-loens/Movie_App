# type: ignore
import requests
import os
from dotenv import load_dotenv
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


def get_movie_data(movie_name: str) -> dict:
    """
    Fetch movie data from the OMDB API.

    Args:
        movie_name (str): The name of the movie to search for.

    Returns:
        dict: The movie data returned by the API.

    Raises:
        ValueError: If API key is missing.
        Exception: For any HTTP or network-related errors.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API key is not set. Please set the API_KEY environment variable.")
    
    url = "http://www.omdbapi.com/"
    params = {
        'apikey': api_key,
        't': movie_name,
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    
    except HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except ConnectionError:
        raise Exception("Connection error. Please check your internet connection.")
    except Timeout:
        raise Exception("The request timed out.")
    except RequestException as err:
        raise Exception(f"An unexpected error occurred: {err}")
