# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： data_operate
Description :
Author : 'li'
date： 2020/10/22
-------------------------------------------------
Change Activity:
2020/10/22:
-------------------------------------------------
"""
from config.database_config import *
from db_operate.data_format import DataFormat
from db_operate.sql_str import ADD_DATA, UPDATE_DATA
from llib.db_utility.mysql_relevant.connection_pool.db_pool import MysqlConnectionPool


class DataOperator:
    def __init__(self):
        self.pool = MysqlConnectionPool(host=DB_IP, user=DB_USER, passwd=DB_PASSWORD,
                                        db=DB_NAME, port=DB_PORT, charset='utf8')

    def add_data(self, data):
        table_name = data['table_name']
        table_name = DataFormat.table_name_format(table_name)
        keys_str = ''
        values_str = ''
        data = data['data']
        for key in data:
            keys_str = keys_str + '`' + key + '`' + ','
            v = data[key]
            v = DataFormat.data_value_format(v)
            values_str = values_str + "'" + v + "'" + ', '
        keys_str = keys_str[:-1]
        values_str = values_str[:-2]
        sql = ADD_DATA.replace('%table_name', table_name) \
            .replace('%fields', keys_str).replace('%values', values_str)
        res = self.pool.execute_sql_str(sql)
        return res

    def update_data(self, data):
        table_name = data['table_name']
        table_name = DataFormat.table_name_format(table_name)
        data = data['data']
        all_content = ''
        for key in data:
            v = data[key]
            v = DataFormat.data_value_format(v)
            values_str = """`$key` = '$value' ,""".replace('$key', key).replace('$value', v)
            all_content = all_content + values_str
        all_content = all_content[:-1]
        sql = UPDATE_DATA.replace('%table_name', table_name) \
            .replace('%update_content', all_content).replace('$unique_id', data['unique_id'])
        res = self.pool.execute_sql_str(sql)
        return res

    def query_data(self, data):
        """
        :return:
        """
        column_info = data['column_info']
        query_content = data['query_content']
        table_name = data['table_name']
        query_data = []
        for info in column_info:
            name = info['COLUMN_NAME']
            data_type = info['DATA_TYPE']
            if data_type in {'文本', '日期', '多行文本'}:
                query_data.append({'name': name, 'type': data_type})
        query_str = 'select * from `%table_name` where 1=1 '.replace('%table_name', table_name)
        for data in query_data:
            name = data['name']
            data_type = data['type']
            if data_type == '文本' or data_type == '多行文本':
                value = query_content[name]
                if len(value) > 0:
                    tmp_str = """  and `%column_name` like '%%value%'  """.replace('%column_name', name) \
                        .replace('%value', value)
                    query_str = query_str + tmp_str
            elif data_type == '日期':
                start_time = query_content[name + '_start'].replace('T', ' ')
                end_time = query_content[name + '_end'].replace('T', ' ')
                if len(start_time) > 5:
                    tmp_start_str = """  and  `%column_name` >= '%start_time' """ \
                        .replace('%column_name', name).replace('%start_time', start_time)
                    query_str = query_str + tmp_start_str
                if len(end_time) > 5:
                    tmp_end_str = """ and  `%column_name` <= '%end_time' """ \
                        .replace('%column_name', name).replace('%end_time', end_time)
                    query_str = query_str + tmp_end_str
        query_str = query_str + ';'
        res = self.pool.select(query_str)
        return res

    def query_by_unique_id(self, table_name, unique_id):
        """
        query by unique id
        :param table_name:
        :param unique_id:
        :return:
        """
        base_sql = """select * from `%table_name` where `unique_id`='%unique_id'""" \
            .replace('%table_name', table_name).replace('%unique_id', unique_id)
        res = self.pool.select(base_sql)
        return res

    def drop_table_by(self, table_name, unique_id):
        """
        query by unique id
        :param table_name:
        :param unique_id:
        :return:
        """
        base_sql = """delete  from `%table_name` where `unique_id`='%unique_id'""" \
            .replace('%table_name', table_name).replace('%unique_id', unique_id)
        res = self.pool.execute_sql_str(base_sql)
        return res


