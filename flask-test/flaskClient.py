import flask
import requests
import base64

ip = '127.0.0.1'
port = 8081
req = 'api/test'

requestUrl = 'http://{}:{}/{}'.format(ip, port, req)

headers = {}

#data = 'Hi'
data = open('fig.png', 'rb').read()

response = requests.post(requestUrl, data=base64.b64encode(data), headers=headers)
print(response.content.decode())
