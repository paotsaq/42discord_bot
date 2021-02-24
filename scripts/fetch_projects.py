# What this script does:
# Fetches all projects from every user in the campus; updates the database into a neat JSON
# currently hardcoded for 42 Lisboa's data; should be easily changeable.

import requests
import get_token as gt
import os
import time
import json

endpoint = '/v2/cursus/1/projects'
CAMPUS_ID = 38

projects = gt.token_request(endpoint).json()
for elem in projects:
	print(projects[0])
