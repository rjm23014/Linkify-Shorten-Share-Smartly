from db import insert_url

BASE_URL = "http://localhost:5000/"

def shorten_url(long_url):
    short_code = insert_url(long_url)
    return BASE_URL + short_code
