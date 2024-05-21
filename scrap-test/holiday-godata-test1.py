import requests
import xmltodict
from pymongo import MongoClient
import os
import requests

api_key = os.environ.get('GODATA_KEY')

url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo'
params ={'serviceKey' : kapi_keyey, 'solYear' : '2024', 'solMonth' : '05' }

response = requests.get(url, params=params)
print(response.status_code)
print(response.content)
data = response.content.decode('utf-8')
print(data)
#exit(0)

# Convert XML to dictionary
data_dict = xmltodict.parse(data)
print(data_dict)
exit(0)
# Connect to MongoDB
client = MongoClient('mongodb://root:root@test.kfs.co.kr:27017/')
db = client['stockdb']
collection = db['days']

collection.insert_one(data_dict)

client.close()