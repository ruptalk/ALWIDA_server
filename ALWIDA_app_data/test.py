import requests


url = "http://localhost:5000/dest/recommend"
# url = "http://ec2-18-179-207-27.ap-northeast-1.compute.amazonaws.com:5000/receipt"

# data = {
#     "name":"test1",
#     "phoneNum":"01012345678",
#     "address":"부산",
#     "carNum":"2425",
#     "id":"test123",
#     "pw":"test123",
#     "agreeCheck":True
# }

# data = {
#     "id":"user1",
#     "pw":"user1"
# }

# data = {
#     "id":"user100",
# }

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

data = {
    "id":"user9",
    "phoneNum":"01011111111",
    "address":"부산",
    "carNum":"123123"
}


res = requests.post(url,data=data)
# res = requests.post(url)
print(res.text)
