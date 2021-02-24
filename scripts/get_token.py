import requests
from dotenv import load_dotenv
import os

load_dotenv()
payload = {
	"grant_type": "client_credentials",
	"client_id": os.environ.get("UID_ID"),
	"client_secret": os.environ.get("SECRET"),
	"scope": "public"
}

api_url = "https://api.intra.42.fr/"
token_endpoint = "oauth/token"
token_result = requests.post(api_url + token_endpoint, params=payload)

options = {
	'page': {
		'number': 0,
		'size': 100,
	}
}

def fetch():
	token = token_result.json()['access_token']
	return token

# this will handle all requests
def token_request(endpoint, options=options):
	token = token_result.json()
	autho = f"{token['token_type']} {token['access_token']}"
	headers = {
		'Authorization': autho
	}
	response = requests.get(api_url + endpoint, json=options, headers=headers)
	if response.status_code != 200:
		raise Exception("Error on token_request")
	return response
