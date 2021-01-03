# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： login_process
Description :
Author : 'li'
date： 2020/12/28
-------------------------------------------------
Change Activity:
2020/12/28:
-------------------------------------------------
"""
import time

from llib.db_utility.mysql_relevant.connection_pool.db_pool import MysqlConnectionPool
from config.database_config import *
from llib.random_utility.uuid_utility import get_uuid_str


class LoginProcessor:
    def __init__(self):
        self.pool = MysqlConnectionPool(host=DB_IP, user=DB_USER,
                                        passwd=DB_PASSWORD, db=DB_NAME,
                                        port=DB_PORT, charset='utf8')
        self.cookies_pool = {}

    def refresh_cookies(self):
        """
        refresh
        :return:
        """
        current_time = time.time()
        for cookies in self.cookies_pool:
            login_time = self.cookies_pool[cookies]
            if current_time - login_time > (3600 * 12):
                try:
                    self.cookies_pool.pop(cookies)
                except:
                    pass

    def check_login_success(self, data):
        self.refresh_cookies()
        username = data['username']
        password = data['password']
        base_sql = """select * from `user_login` where `username`= '%username%' and `password`='%password%'; """ \
            .replace('%username%', username).replace('%password%', password)
        res = self.pool.select(base_sql)
        if len(res) == 0:
            return ''
        cookies = get_uuid_str()
        self.cookies_pool[cookies] = time.time()
        return cookies

    def check_cookies_valid(self, data):
        self.refresh_cookies()
        cookie = data['cookie']
        if cookie in self.cookies_pool:
            return 'True'
        return 'False'


LOGIN_PROCESSOR = LoginProcessor()
