import requests

url = 'http://localhost:8000/api/transactions'


headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer 47061d41-7994-4fad-99a7-54879acd9a83'
}

r = requests.get(url, headers=headers)
print(r.text)
