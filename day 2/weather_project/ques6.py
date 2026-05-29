import requests
import sys

url = "https://api.github.com/users/anthropics"

try:
	response = requests.get(url)
	
	if response.status_code == 200:
		data = response.json()
		print("Name:", data["name"])
		print("Public Repos:", data["public_repos"])
		print("Followers:",data["followers"])
	else:
		print(f"Error : request failed to fetch data (Status Code: {response.status_code})")
		sys.exit(1)
except requests.RequestException as e:
	print("Request Failed:",e)
	sys.exit(1)
