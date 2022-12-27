import requests


url = "http://localhost:5000/receipt"
# url = "http://ec2-18-179-207-27.ap-northeast-1.compute.amazonaws.com:5000/container_state"

# data = {
#     "name":"test",
#     "phoneNum":"01012345678",
#     "address":"부산",
#     "carNum":"2425",
#     "id":"test",
#     "pw":"test",
#     "agreeCheck":True
# }

# data = {
#     "id":"user1",
#     "pw":"user111"
# }

data = {
    "id":"user2",
}

# data = {
#     "id":"user1",
#     "containerNum":"1111",
#     "location":"부산신항",
#     "terminal":"국제신항",
#     "hour":12,
#     "minute":36
# }

# data = {
#     "id":"user1",
#     "hour":15,
#     "minute":30
# }

# data = {
#     "containerNum":""
# }

# data = {
#     "id":"user1",
#     "phoneNum":"01011111111",
#     "address":"부산",
#     "carNum":"2222"
# }


res = requests.post(url,data=data)
# res = requests.post(url)
print(res.text)
