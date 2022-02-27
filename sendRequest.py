import requests
from config import credentials

def sendRequest(pcRequest):
    response = requests.get(pcRequest, auth=(credentials.username, credentials.secret))
    data = response.json()['data']
    return (data)