import requests
url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)
if response.status_code==200:
    users = response.json()
    for user in users:
        print("Name:",user["name"])
        print("Email:",user["email"])
        print("-"*30)
else:
    print("Request Failed")