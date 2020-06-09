import requests
from test.utils import sm4
from test.utils.readconfig import config
import json

class myrequest:
    def post(self,url,data):
        key = config().getconfig("jl", "key")
        encrypt_data=sm4.sm4encrype(key,str(data))
        md5_data=sm4.getmd5(encrypt_data)
        url=url+md5_data
        res=requests.post(url,encrypt_data)
        res_data =sm4.sm4decrypt(key,res.content)
        return json.loads(res_data)


if __name__ == "__main__":
    url="http://10.10.22.236:8941/secret/common/lottLogin?partnerId=00101&hashType=md5&hash="
    data="{'PartnerId': '00101', 'SerialNum': '2016040003', 'Version': '1.0.0.0', 'Token': '2016040003', 'ReqContent': {'Userid': '2290110100003', 'LoginPass': '123456', 'LoginType': '1', 'MacAddress': 'ABCDEFG123456'}, 'TimeStamp': 'now'}"
    res=myrequest().post(url,data)
    print(res)
    print(res['RespContent']['LoginSession'])