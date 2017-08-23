import os
import requests

API_KEY = os.environ.get("BREWERYDB_API_KEY", "af61821855950bcb410d9560794c7c02")
API_ROOT = "https://api.brewerydb.com/v2/{{path}}?key={key}&".format(key=API_KEY)


def get_beer_by_abv(abv):
    path = "beers"
    params = [
        "abv={}".format(abv),
        "hasLabels=Y",
    ]
    url = API_ROOT.format(path=path) + "&".join(params)
    print(url)
    return requests.get(url)
