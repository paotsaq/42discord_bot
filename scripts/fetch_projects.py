# What this script does:
# Fetches all projects from every user in the campus; updates the database into a neat JSON
# currently hardcoded for 42 Lisboa's data; should be easily changeable.

import requests
import get_token as gt
import os
import time
import json

APINTO = 80752
CAMPUS_ID_42LISBOA = 38
campus_users_endpoint = f'v2/campus/{CAMPUS_ID_42LISBOA}/users'
user_projects_endpoint = f'/v2/users/{APINTO}/projects_users'
response = gt.token_request(user_projects_endpoint).json()
print(response[0])
for project in response:
	print(project['project']['name'])
