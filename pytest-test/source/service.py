import requests
database = {
    1 : "John",
    2 : "Doe",
    3 : "Jane",
    4 : "Hong"
}

def get_user_from_db(id):
    return database[id]

def get_users():
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    if response.status_code == 200:
        return response.json()
    
    raise requests.HTTPError(response.status_code)
