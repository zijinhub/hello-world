# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : scp_rewrite
# @FileName : toolkit.py.py
# @Time : 2020/5/6 17:13
# @Author : Nick


import hashlib
import json
import time
import requests
from test.data_handle2  import init_config
from test.data_handle2 import sm4decode
from test.data_handle2.init_config import basic_data


class Toolkit:
    @classmethod
    def time_stamp_gen(cls):
        # 生成服务器时间时间戳
        time_req = {
            "PartnerId": basic_data.partner_id,
            "TimeStamp": basic_data.current_time(),
            "SerialNum": basic_data.serial_num_gen(),
            "Version": basic_data.version,
            "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "ReqContent": {
            }
        }
        return Toolkit.executive_test(basic_data.time_sync_profix_url + basic_data.partner_id + '&hashType=md5&hash=',
                                     'time', time_req)

    @classmethod
    def session_id(cls):
        server_time_stamp = Toolkit.time_stamp_gen()
        req_content = {
            "PartnerId": basic_data.partner_id,
            "TimeStamp": server_time_stamp,
            "SerialNum": basic_data.serial_num_gen(),
            "Version": basic_data.version,
            "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "ReqContent": {
                "Userid": "",
                "LoginPass": "",
                "LoginType": "",
                "MacAddress": ""
            }
        }
        req_content['ReqContent']["Userid"] = basic_data.user_id
        req_content['ReqContent']["LoginPass"] = basic_data.login_pass
        req_content['ReqContent']["MacAddress"] = basic_data.mac_address
        req_content['ReqContent']["LoginType"] = basic_data.login_type
        print('req_content:', req_content)
        basic_data.logger.info("登录开始")
        return Toolkit.executive_test(basic_data.login_profix_url + basic_data.partner_id + '&hashType=md5&hash=',
                                     'login', req_content)

    @classmethod
    def md5(cls, dt):
        """进行md5加密"""
        h1 = hashlib.md5()
        h1.update(dt)
        return h1.hexdigest().upper()

    @classmethod
    def check_code(cls, in_string):
        """获取MD5校验码"""
        ret = 0
        for i in range(len(in_string)):
            ret = ret + ord(in_string[i])
        ret = ret % 100000
        out_string = str(ret)
        for i in range(5 - len(out_string)):
            out_string = "0" + out_string
        return out_string

    @classmethod
    def current_time(cls):
        # 生成当前时间时间戳
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    @classmethod
    def req_set_url(cls, profix_url = None, hash_content = None):
        # basic_data.logger.debug("0 进入URL地址组装函数")
        return profix_url + str(hash_content)

    @classmethod
    def req_set_md5(cls, raw_data, key = ''):
        # 使用separators参数去掉dumps生成的字符串中逗号和冒号后面的空格
        json_string = json.dumps(raw_data, separators = (',', ':'))
        # sm4加密
        md5_bytes = sm4decode.sm4encrype(key, json_string)
        # md5加密
        md5_hash = Toolkit.md5(md5_bytes)
        return md5_bytes, md5_hash

    @classmethod
    def decode_recv_data(cls, recv_data, key = ''):
        # 解密返回数据，得到String类型的数据
        recv_byte_array = sm4decode.sm4decrypt(key, recv_data.content)

        return json.loads(recv_byte_array)

    @classmethod
    def executive_test(cls, profix_url, interface_type, content):
        if interface_type in ["login", "sell", "encash", 'encash_sell']:
            md5, md5_hash = Toolkit.req_set_md5(content, key = basic_data.gm_key)
            # basic_data.logger.info('0 进入"login", "sell", "encash"接口处理过程')
            basic_data.logger.debug('Hash值返回成功，md5_hash: %s' % md5_hash)
            basic_data.logger.debug('md5加密后数据返回成功')
            test_url = Toolkit.req_set_url(profix_url, md5_hash)
            basic_data.logger.debug('URL组装成功，test_url: %s' % test_url)
            # print("url: ", test_url)
            recv = requests.post(test_url, data = md5, timeout=5)
            # 查看返回结果
            # print("recv.content", recv.content)
            recv_post = Toolkit.decode_recv_data(recv, key = basic_data.gm_key)
            # basic_data.logger.info('返回值解密成功，recv_post: %s' % recv_post)
            # print("recv_post", recv_post)
            if interface_type == 'sell' and recv_post["BackCode"] == '100000' or \
                    interface_type == 'encash_sell' and recv_post["BackCode"] == '100000':
                db_connect = init_config.db_connection()
                try:
                    with db_connect.cursor() as cursor:
                        if interface_type == 'sell':
                            sql = "INSERT INTO sell_result (Runcode,TicketCode, SellTime,AccountDate,ExtraCode," \
                                  "PlayEname,SellTermCode)values (%s,%s,%s,%s,%s,%s,%s);"
                        if interface_type == 'encash_sell':
                            sql = "INSERT INTO sell_result_for_encash (Runcode,TicketCode, SellTime,AccountDate," \
                                  "ExtraCode,PlayEname,SellTermCode)values (%s,%s,%s,%s,%s,%s,%s);"
                        cursor.execute(sql, (recv_post['RespContent']['RunCode'], recv_post['RespContent']['TicketCode'],
                                             recv_post['RespContent']['SellTime'], recv_post['RespContent']['AccountDate'],
                                             recv_post['RespContent']['ExtraCode'], content['ReqContent']['PlayEname'],
                                             content['ReqContent']['SellTermCode']))
                        db_connect.commit()
                finally:
                    db_connect.close()
            if interface_type == 'login' and "RespContent" in recv_post:
                basic_data.logger.debug('Login接口返回成功，recv_post["RespContent"][“LoginSession”]: %s' %
                                        recv_post["RespContent"]['LoginSession'])
                return recv_post["RespContent"]['LoginSession']

        elif interface_type in ["time", "bet_query", "account_query"]:
            # basic_data.logger.info('0 进入"time", "bet_query", "account_balance"接口处理过程')
            md5, md5_hash = Toolkit.req_set_md5(content, key = basic_data.old_key)
            basic_data.logger.debug('Hash值返回成功，md5_hash: %s' % md5_hash)
            basic_data.logger.debug('md5加密后数据返回成功')
            # print(md5)
            test_url = Toolkit.req_set_url(profix_url, md5_hash)
            basic_data.logger.debug('URL组装成功，test_url: %s' % test_url)
            # print("url: ", test_url)
            recv = requests.post(test_url, data = md5)
            # print("http code:", recv.status_code)
            recv_post = Toolkit.decode_recv_data(recv, key = basic_data.old_key)
            # basic_data.logger.info('返回值解密成功，recv_post: %s' % recv_post)
            # print(recv_post)
            if interface_type == 'time' and "RespContent" in recv_post:
                # print('SysDateTime', recv_post["RespContent"]['SysDateTime'])
                basic_data.logger.info('time接口返回成功，time: %s' % recv_post["RespContent"]['SysDateTime'])
                return recv_post["RespContent"]['SysDateTime']
        basic_data.logger.info('接口返回成功，recv_post %s' % recv_post)
        return recv_post

