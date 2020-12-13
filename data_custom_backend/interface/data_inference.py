# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： table_inference
Description :
Author : 'li'
date： 2020/10/21
-------------------------------------------------
Change Activity:
2020/10/21:
-------------------------------------------------
"""
import json

from db_operate.data_operate import DataOperator

data_operator = DataOperator()


class DataInterface:
    @staticmethod
    def add_data(data):
        """
        add data
        :param data:
        :return:
        """
        res = data_operator.add_data(data)
        if res['result']:
            return json.dumps({'msg': '添加数据成功', 'is_success': True})
        else:
            return json.dumps({'msg': '添加数据失败', 'is_success': False})

    @staticmethod
    def update_data(data):
        """
        add data
        :param data:
        :return:
        """
        res = data_operator.update_data(data)
        if res['result']:
            return json.dumps({'msg': '添加数据成功', 'is_success': True})
        else:
            return json.dumps({'msg': '添加数据失败', 'is_success': False})

    @staticmethod
    def query_data(data):
        """
        query_data
        :param data:
        :return:
        """
        res = data_operator.query_data(data)
        format_data = {}
        new_lst = []
        for r in res:
            r['check'] = ''
            new_lst.append(r)
        format_data['data'] = new_lst
        return json.dumps(format_data)
        # return json.dumps({'msg': res, 'is_success': True})

    @staticmethod
    def format_data(data):
        """
        format data
        :param data:
        :return:
        """
        if len(data) == 0:
            return None
        keys = data[0].keys()
        values = []
        for v in data:
            row = []
            for k in keys:
                row.append(v[k])
            values.append(row)
        return {'column_names': list(keys), 'rows': values}

    @staticmethod
    def parse_query_data(data):
        """
        parse query data
        :param data:
        :return:
        """
        pass

    @staticmethod
    def query_data_by_unique_id(data):
        """

        :param data:
        :return:
        """
        table_name = data['table_name']
        unique_id = data['unique_id']
        res = data_operator.query_by_unique_id(table_name, unique_id)[0]
        return json.dumps(res)

    @staticmethod
    def delete_data_post(data):
        table_name = data['table_name']
        unique_id = data['unique_id']
        exe_result = data_operator.drop_table_by(table_name, unique_id)
        if exe_result['result']:
            return json.dumps({'msg': '删除成功', 'is_success': True})
        else:
            return json.dumps({'msg': '删除失败', 'is_success': False})
