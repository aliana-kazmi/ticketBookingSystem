import requests

BASE = "http://127.0.0.1:5000/"
response = requests.post(BASE + 'ticket',{'user_id':3,'issue':'add x to X'})

# response = requests.post(BASE + 'ticket',{'user_id':1,'issues':'add x to X'})
print(response.json())