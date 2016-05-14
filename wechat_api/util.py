import hashlib
import requests

def check_signature(signature, timestamp, nonce, token):
    pwd = "".join(sorted([token, timestamp, nonce]))
    return hashlib.sha1(pwd).hexdigest() == signature

def get_access_token()
