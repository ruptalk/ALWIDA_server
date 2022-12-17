import requests


url = "http://localhost:5000/reservation_state"
# url = "http://ec2-18-179-207-27.ap-northeast-1.compute.amazonaws.com:5000/signup_id"

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
    "id":"user1"
}

# data = {
#     "id":"user1",
#     "location":"부산신항",
#     "name":"국제신항",
#     "time":"2022-12-17"
# }

res = requests.post(url,data=data)
# res = requests.post(url)
print(res.text)
