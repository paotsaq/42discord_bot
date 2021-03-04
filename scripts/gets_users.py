# What this script does:
# Fetches all users from the campus, retaining unique ID's. Makes a json database matching name to ID.
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
		users[info['login']] = {}
		users[info['login']]['id'] = info['id']
		user_endpoint = f'v2/users/{info["id"]}'
		tries = 0
		success = 0
		while (tries < 3 and not success):
			try:
				response = gt.token_request(user_endpoint).json()
				if 21 == response['cursus_users'][1]['cursus_id']:
					users[info['login']]['is_student'] = True
				print(f"user {[info['login']]} added!")
				success = 1
				break
			except IndexError:
				break
			except Exception:
				time.sleep(2)
				tries += 1
				print('wasting time!')

	i += 1
dj.dump_to_json("users_ids", users)
