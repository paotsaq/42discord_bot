TOKEN_PROD = "Nzc3NjQwNDQ0NDk4MjgwNDU4.X7GYGQ.XWmsqxcr96bPYrF3iPRUd_4ddAY"
TOKEN_DEV = "NzgzNzMzMDM2MDYyOTk4NTc5.X8fCRA.m4_B5qyGM4pKUY2SVjn_O1-VK-g"
UID_ID = "1c643ac91cbe1209a4f7efc24569b487c306fed13b7d0cebeaa3e9d1e97dabb4"
SECRET = "86e7b46c0f5029e18e5b0de883087f45a4646c134fa670f27805adfc8e1b08c1"

import requests

payload = {
    "grant_type": "client_credentials",
    "client_id": UID_ID,
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
coalitions = [FLINSTONES_ID, SIMPSONS_ID, JETSONS_ID]
for team in coalitions:
    endpoint = f"v2/coalitions/{team}/users"
    info = requests.get(api_url + endpoint, headers=headers)
    print(info.json())

another_thing = print(another_thing.json())
