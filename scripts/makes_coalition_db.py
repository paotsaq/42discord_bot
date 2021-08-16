# What this script does:
# Fetches all users from a given set of coalitions from the 42 API; updates the database into a neat JSON
# currently hardcoded for 42 Lisboa's coalitions; should be easily changeable.

import requests
from dotenv import load_dotenv
import os
import time
import json

load_dotenv()
payload = {
		"grant_type": "client_credentials",
		"client_id": os.environ.get("UID_ID"),
		"client_secret": os.environ.get("SECRET"),
		"scope": "public"
	}

FLINSTONES_ID = 121
SIMPSONS_ID = 120
JETSONS_ID = 119
coalitions = [FLINSTONES_ID, SIMPSONS_ID, JETSONS_ID]

api_url = "https://api.intra.42.fr/"
token_endpoint = "oauth/token"
coal_endpoint = "v2/coalitions"
autho = ""
headers = {}

def crawler():
	def token_handler():
		global autho
		global headers
		token_result = requests.post(api_url + token_endpoint, params=payload)
		token = token_result.json()['access_token']
		autho = f"{token_result.json()['token_type']} {token}"
		headers = {
			'Authorization': autho
		}
	token_handler()
	users = {}
	total = 0
	options = {
		'page': {
			'number': 0,
			'size': 100,
		}
	}
	for team in coalitions:
		endpoint = f"v2/coalitions/{team}/users"
		options['page']['number'] = 0
		finished = 0
		users[team] = []
		while not finished:
			coalition_members = []
			options['page']['number'] += 1
			response = requests.get(api_url + endpoint, json=options, headers=headers)
			if response.status_code != 200:
				return
			info = response.json()
			print(f"fetching page {options['page']['number']} for coalition number {coalitions.index(team) + 1}")
			time.sleep(0.3)
			if len(info) != 0:
				for elem in info:
					coalition_members.append(elem['login'])
				users[team] += coalition_members
			else:
				finished = 1
	print(users)
	return users
