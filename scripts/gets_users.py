# What this script does:
# Fetches all users from the campus, retaining unique ID's. Updates the database into a neat JSON
# currently hardcoded for 42 Lisboa's data; should be easily changeable.

import requests
import get_token as gt
import os
import time
import json
import dump_to_json as dj

CAMPUS_ID_42LISBOA = 38
campus_users_endpoint = f'v2/campus/{CAMPUS_ID_42LISBOA}/users'
i = 1
users = {}
while (i == 1 or response != []):
	response = gt.token_request(campus_users_endpoint, i).json()
	for info in response:
		users[info['login']] = info['id']
	i += 1
dj.dump_to_json("users_ids", users)
