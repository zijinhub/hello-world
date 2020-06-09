import requests
import json
data={'username':'hzj','email':'123456'}

res=requests.post('http://127.0.0.1:8000/web/adduser/',data=data)
print(res.text)