    "client_secret": SECRET,
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
coalitions = [FLINSTONES_ID, SIMPSONS_ID, JETSONS_ID]
users = {}
for team in coalitions:
	endpoint = f"v2/coalitions/{team}/users"
	while options['page']['number'] != 5:
		coalition_members = []
		options['page']['number'] += 1
		info = requests.get(api_url + endpoint, headers=headers).json()
		print(f"another batch! page number {options['page']['number']}\nnumber of members: {len(info)}")
		for elem in info:
			coalition_members.append(elem['login'])

