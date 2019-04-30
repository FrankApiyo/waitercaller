import requests
import json

def shorten_url(longurl):
    linkRequest = {
    "destination": longurl,
    "domain": { "fullName": "rebrand.ly" }
    }

    requestHeaders = {
    "Content-type": "application/json",
    "apikey": "5c9250e0483a4e3d81b856cddcca551d",
    }

    r = requests.post("https://api.rebrandly.com/v1/links", 
    data = json.dumps(linkRequest),
    headers=requestHeaders)

    if (r.status_code == requests.codes.ok):
        link = r.json()
        return link["shortUrl"]
    else: 
        return longurl

