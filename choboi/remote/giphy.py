import os
import logging
import requests

API_KEY = os.environ.get("GIPHY_CHOBOI_API_KEY", "ce52ff2d31814b4ca40c6bb24ea97dda")
API_ROOT = "https://api.giphy.com/v1/gifs/{endpoint}"

logger = logging.getLogger(__name__)


def get_random_gif_by_tag(tag):
    logger.info("fetching gif by tag %s", tag)
    endpoint = 'random'
    address = API_ROOT.format(endpoint=endpoint)
    params = {'api_key': API_KEY, 'tag': tag, 'rating': 'g'}
    response = requests.get(address, params=params)
    logger.info("fetched image with %s status code", response.status_code)
    return response
