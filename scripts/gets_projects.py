# What this script does:
# Fetches all (42 cursus) projects from any user. Makes a json database matching name to ID.
# currently hardcoded for 42 Lisboa's data; should be easily changeable.

import requests
import get_token as gt
import os
import time
import json
import dump_to_json as dj

LIBFT_ID = 1314
CAMPUS_ID_42LISBOA = 38
CURSUS_ID = 21

with open("database/users_ids.json", 'r') as file:
	user_db = json.load(file)

cursus_endpoint = '/v2/cursus/21/cursus_users'
options = {
	'filter' = {
		'campus_id' = CAMPUS_ID_42LISBOA
	}
}

print(user_db)
for user in user_db:
	endpoint = f'/v2/users/{user_db[user]}/projects_users'
	response = gt.token_request(endpoint).json()
	if
