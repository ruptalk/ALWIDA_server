import requests


url = "http://localhost:5000/signup"

data = {
    "name":"양강민",
    "phoneNum":"01092337395",
    "address":"부산",
    "carNum":"2425",
    "id":"hogbal",
    "pw":"hogbal",
    "agreeCheck":True
}

res = requests.post(url,data=data)
print(res.text)
