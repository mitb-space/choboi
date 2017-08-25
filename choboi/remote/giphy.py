import os
import requests

API_KEY = os.environ.get("GIPHY_CHOBOI_API_KEY", "ce52ff2d31814b4ca40c6bb24ea97dda")
API_ROOT = "https://api.giphy.com/v1/gifs/{endpoint}/"


def get_random_gif_by_tag(tag):
    endpoint = 'random'
    address = API_ROOT.format(endpoint=endpoint)
    params = {'api_key': API_KEY, 'tag': tag, 'rating': 'g'}
    response = requests.get(address, params=params)
    print(response.url)
    return response
