import requests


url = "http://localhost:5000/signup/id"
# url = "http://ec2-18-179-207-27.ap-northeast-1.compute.amazonaws.com:5000/receipt"

# data = {
#     "name":"hogbal",
#     "phoneNum":"01012345678",
#     "address":"부산",
#     "carNum":"2425",
#     "id":"hogbal",
#     "pw":"hogbal",
#     "agreeCheck":True
# }

# data = {
#     "id":"user1",
#     "pw":"user1"
# }

data = {
    "id":"user1",
}

# data = {
#     "id":"hogbal",
#     "containerNum":"1111",
#     "location":"부산신항",
#     "terminal":"국제신항",
#     "hour":6,
#     "minute":30
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
#     "id":"user9",
#     "phoneNum":"01011111111",
#     "address":"부산",
#     "carNum":"123123"
# }

# data = {
#     "id":"hogbal",
#     "congestion":True
# }

# files = open('test.jpeg','rb')
# upload = {'file':files}
# print(files)
# res = requests.post(url, data=data, files=upload)

res = requests.post(url,data=data)
print(res.text)
