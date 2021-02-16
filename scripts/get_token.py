import requests
from dotenv import load_doten

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
