import os
from dotenv import load_dotenv
import requests

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REPOS = os.getenv("REPOS")

issuesurl = "https://api.github.com/repos/"+REPOS+"/issues"

params = {
    'page': '1',
    'per_page': '100'
}

response = requests.get(
    issuesurl,
    params = params,
    headers = {
        'Authorization': 'Bearer '+ACCESS_TOKEN
    }
)

print(response.json())