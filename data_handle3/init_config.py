# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : scp_rewrite
# @FileName : init_config.py
# @Time : 2020/5/7 16:59
# @Author : Nick
import configparser
import logging
import random
import time
import pathlib
import pytest
import pymysql
from test.utils.readconfig import config

def db_connection():
    """
        读取pytest.ini中关于数据库的配置项db并连接数据库
        :return: 返回一个数据库连接对象
        """
    try:


        db_host =config().getconfig('DB','host')

        db_user = config().getconfig('DB', 'user')
        db_pwd = config().getconfig('DB', 'password')
        print(db_pwd)
        db = config().getconfig('DB', 'db')
        db_charset = config().getconfig('DB', 'charset')
        connection = pymysql.connect(host = db_host, user = db_user, password = db_pwd, db = db,
                                     charset = db_charset,
                                     cursorclass = pymysql.cursors.DictCursor)
        print('DB:', type(connection))
        return connection
    except Exception as e:
        print("读取配置文件或连接数据库错误：", e)


def get_db_data(sql, count):
    """
    从数据库查询数据，并返回指定的记录条数
    :param sql: SQL查询语句
    :param count: 指定要返回记录的条数，默认返回所有查询结果。
    :return: 返回一个数据集列表，每个列表元素代表一条记录
    """
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            # 注意采坑：这里的SQL语句要和mysql语法要完全一样
            cursor.execute(sql)
            # 选择返回的数据数量，暂时为了测试只选择4条
        if count == 'all':
            result = cursor.fetchall()

        else:
            result = cursor.fetchmany(int(count))
            print(result)
        connection.close()
        return result
    except Exception as e:
        print("读取配置文件或连接数据库错误：", e)


class DataSet(object):
    """
    读取配置文件中的配置项，并以单例模式的方式返回
    """
    __instance = None

    def __init__(self):
        # 读取配置文件中关于java和jar的配置项
        # config = configparser.ConfigParser()
        # pytest_path = pathlib.Path('pytest.ini')
        # config.read(str(pytest_path))
        # print(config.sections())

        # 接口URL前缀
        self.sell_profix_url = config().getconfig('Url_set', 'sell_profix')
        self.time_sync_profix_url = config().getconfig('Url_set', 'time_sync_profix')
        self.encash_profix_url = config().getconfig('Url_set', 'encash_profix')
        self.bet_query_url = config().getconfig('Url_set', 'bet_query_profix')
        self.account_query_url = config().getconfig('Url_set', 'account_query_profix')
        self.login_profix_url = config().getconfig('Url_set', 'login_profix')

        # 登录、投注、兑奖3个接口使用
        self.gm_key = config().getconfig('Key', 'gm_key')
        # 3个查询接口使用（时间同步、自购投注查询、站点余额）
        self.old_key = config().getconfig('Key', 'old_key')

        # 在数据库中取一条mac_address不为空的终端信息
        terminal_info = get_db_data("SELECT terminal_id, mac_address, channel_id FROM unity_self_terminal "
                                    "WHERE terminal_id = '2290110100001';",  '1')
        terminal_info[0]["LoginPass"] = "123456"
        # 自助终端的编号
        self.user_id = terminal_info[0]['terminal_id']
        # MAC地址
        self.mac_address = terminal_info[0]['mac_address']
        # 渠道ID
        self.partner_id = terminal_info[0]['channel_id']
        # 版本
        self.version = config().getconfig('Basic_info', 'version')
        # 登录密码
        self.login_pass = terminal_info[0]["LoginPass"]
        # 登录类型
        self.login_type = config().getconfig('Basic_info', 'logintype')
        # 日志记录器
        log_temp = logging.basicConfig(level = logging.INFO,
                                       format = '%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)6s)')
        self.logger = logging.getLogger(log_temp)

        # 取新期
        new_terms = get_db_data("SELECT play_ename,MAX(term_code) FROM hot_term  GROUP BY play_ename;", 'all')
        for item in new_terms:
            if item['play_ename'] == 'B001':
                self.ball_term_code = item['MAX(term_code)']
            if item['play_ename'] == 'K3':
                self.k3_term_code = item['MAX(term_code)']
            if item['play_ename'] == 'QL730':
                self.QL730_term_code = item['MAX(term_code)']
            if item['play_ename'] == 'S3':
                self.d3_term_code = item['MAX(term_code)']

    @classmethod
    def serial_num_gen(cls):
        # 生成15位随机列号
        return str(random.randrange(1, 9999)) + str(random.randrange(1, 9999)) + str(random.randrange(1, 9999))

    @staticmethod
    def serial_num_gen():
        # 生成15位随机列号
        return str(random.randrange(1, 9999)) + str(random.randrange(1, 9999)) + str(random.randrange(1, 9999))

    @staticmethod
    def current_time():
        # 生成当前时间时间戳
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance


basic_data = DataSet()

print(basic_data.d3_term_code)
