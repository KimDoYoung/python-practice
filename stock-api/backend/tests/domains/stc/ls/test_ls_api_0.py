from dotenv import load_dotenv
import os

import requests

# Load variables from .env file
load_dotenv()

# Access the variables
APP_KEY = os.getenv("LS_APP_KEY")
APP_SECRET = os.getenv("LS_APP_SECRET")

# Use the variables in your code
print(f"APP_KEY={APP_KEY}")
print(f"APP_SECRET={APP_SECRET}")

header = {"content-type":"application/x-www-form-urlencoded"}
param = {"grant_type":"client_credentials", "appkey":APP_KEY, "appsecretkey":APP_SECRET,"scope":"oob"}
PATH = "oauth2/token"
BASE_URL = "https://openapi.ls-sec.co.kr:8080"
URL = f"{BASE_URL}/{PATH}"
request = requests.post(URL, verify=False, headers=header, params=param)
ACCESS_TOKEN = request.json()["access_token"]
print(f"ACCESS_TOKEN: {ACCESS_TOKEN}") 

# Save the ACCESS_TOKEN to the .env file
with open(".env", "a") as f:
    f.write(f"\nLS_ACCESS_TOKEN={ACCESS_TOKEN}")