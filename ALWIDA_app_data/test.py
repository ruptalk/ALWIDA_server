import requests


# url = "http://localhost:5000/signup"
url = "http://ec2-18-179-207-27.ap-northeast-1.compute.amazonaws.com:5000/signup_id"

# data = {
#     "name":"양강민",
#     "phoneNum":"01092337395",
#     "address":"부산",
#     "carNum":"2425",
#     "id":"hogbal",
#     "pw":"hogbal",
#     "agreeCheck":True
# }

# data = {
#     "id":"user1",
#     "pw":"user2"
# }

data = {
    "id":"user1123"
}

res = requests.post(url,data=data)
print(res.text)
