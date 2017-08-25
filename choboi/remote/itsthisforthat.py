import logging
import requests

logger = logging.getLogger(__name__)

ITSTHISFORTHAT_API_ADDRESS = "http://itsthisforthat.com/api.php?json"

def get_random_app_idea():
    logger.info("fetching random app idea")
    response = requests.get(ITSTHISFORTHAT_API_ADDRESS)
    return response
