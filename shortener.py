import hashlib

BASE_URL = "http://localhost:5000/"

def shorten_url(long_url):
    hash_object = hashlib.md5(long_url.encode())
    short_hash = hash_object.hexdigest()[:6]
    return BASE_URL + short_hash
