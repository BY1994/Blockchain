import requests
import json

headers = {'Content-Type' : 'application/json; charset=utf-8'}
data = {
    "sender": 1004,
    "recipient": 0,
    "amount": 1004,
}
print(requests.post("http://localhost:5000/transactions/new", headers=headers, data=json.dumps(data)).content)