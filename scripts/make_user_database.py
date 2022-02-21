# What this script does:
# Fetches all users from the 42 API, matching the Lisboa campus; updates the database into a neat JSON

from scripts.dump_to_json import *
import requests
from dotenv import load_dotenv
import os
import time
import json
import logging
import pprint

load_dotenv()
payload = {
		"grant_type": "client_credentials",
		"client_id": os.environ.get("UID_ID"),
		"client_secret": os.environ.get("SECRET"),
		"scope": "public"
}

api_url = "https://api.intra.42.fr/"
token_endpoint = "oauth/token"
autho = ""
headers = {}

# TODO This should be in a separate file.
def token_handler():
	global autho
	global headers
	token_result = requests.post(api_url + token_endpoint, params=payload)
	try:
		print(token_result)
		token = token_result.json()['access_token']
		logging.info("Successfully obtained access token.")
	except KeyError:
		return
	autho = f"{token_result.json()['token_type']} {token}"
	headers = {
		'Authorization': autho
	}

def get_campus_students():
	number = 1
	res = {}
	while number == 1 or len(response.json()) != 0:
		url = f"https://api.intra.42.fr/v2/cursus_users?page[size]=100&page[number]={number}&cursus_id=21&filter[campus_id]=38"
		response = requests.get(url, headers=headers, data=payload)
		try:
			logging.info(f"Currently at student {response.json()[0]['user']['login']}")
			new_dic = create_dictionary_from_response(response.json())
			res.update(new_dic)
		except IndexError:
			logging.debug("Requests are finished.")
		number += 1
	return res

# fetches all users from the campus,
# and returns a dictionary

def create_dictionary_from_response(response):
	res = {}
	for elem in response:
		res.update({elem['user']['login']: elem['user']['id']})
	return res

def create_user_database():
	token_handler()
	if autho == "":
		return
	res = get_campus_students()
	dump_to_json(res, "users_id_database")
