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

api_url = "https://api.intra.42.fr/"
endpoint = "oauth/token"

token_result = requests.post(api_url + endpoint, params=payload)
token = token_result.json()['access_token']

endpoint = "v2/coalitions"
autho = f"{token_result.json()['token_type']} {token}"
headers = {
    'Authorization': autho
    }

coalitions = requests.get(api_url + endpoint, headers=headers)
FLINSTONES_ID = 121
SIMPSONS_ID = 120
JETSONS_ID = 119

total = 0
options = {
	'page': {
		'number': 0,
		'size': 100,
	}
}
users = {}
coalitions = [FLINSTONES_ID, SIMPSONS_ID, JETSONS_ID]
for team in coalitions:
	endpoint = f"v2/coalitions/{team}/users"
	options['page']['number'] = 0
	finished = 0
	users[team] = []
	while not finished:
		coalition_members = []
		options['page']['number'] += 1
		response = requests.get(api_url + endpoint, json=options, headers=headers)
		info = response.json()
		print("letting it rest...")
		time.sleep(4)
		if len(info) != 0:
			for elem in info:
				coalition_members.append(elem['login'])
			users[team] += coalition_members
		else:
			finished = 1

json_file = open("database/coalition_users.json", 'w')
json.dump(users, json_file, ensure_ascii=False, indent=2)
json_file.close()

