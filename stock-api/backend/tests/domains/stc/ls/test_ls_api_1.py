import json
from dotenv import load_dotenv
import os

import requests

# Load variables from .env file
load_dotenv()

# Access the variables
APP_KEY = os.getenv("LS_APP_KEY")
APP_SECRET = os.getenv("LS_APP_SECRET")
ACCESS_TOKEN = os.getenv("LS_ACCESS_TOKEN")

# Use the variables in your code
print(f"APP_KEY={APP_KEY}")
print(f"APP_SECRET={APP_SECRET}")
print(f"ACCESS_TOKEN={ACCESS_TOKEN}")

# 개별종목 현재가 및 기간별 시세 
BASE_URL = "https://openapi.ls-sec.co.kr:8080"
headers = {
            "Content-Type": "application/json; charset=utf-8",
            "authorization" : "Bearer " + ACCESS_TOKEN,
            "tr_cd" : "t1101",
            "tr_cont" : "N",
            "tr_cont_key" : "",
            "mac_address" : ""
        }
data = {
            "t1101InBlock" : { "shcode" : "005930"  }
        }
PATH = "/stock/market-data"
URL = f"{BASE_URL}/{PATH}"
response = requests.post(URL, headers=headers, data=json.dumps(data))
print(response.json())
