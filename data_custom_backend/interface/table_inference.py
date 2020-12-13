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

from db_operate.data_format import DataFormat
from db_operate.sql_str import ADD_COLUMN, DELETE_COLUMN
from db_operate.table_operate import TableOperator

table_operator = TableOperator()


class TableInterface:
    @staticmethod
    def create_table(data):
        table_name = data['table_name']
        columns = data['columns']
        table_comment = data['table_comment']
        result = table_operator.create_table_name(table_name, columns, table_comment)
        if result:
            return json.dumps({'msg': '添加表成功', 'is_success': True})
        else:
            return json.dumps({'msg': '添加表失败', 'is_success': False})

    @staticmethod
    def search_table(data):
        table_name = data['table_name']
        result = table_operator.query_table_name(table_name)
        return json.dumps({"data": result})

    @staticmethod
    def get_table_comment(data):
        table_name = data['table_name']
        result = table_operator.query_table_comment(table_name)
        return json.dumps({"data": result})

    @staticmethod
    def alter_table_name(data):
        old_name, new_name = data['old_name'], data['new_name']
        result = table_operator.alter_table_name(old_name, new_name)
        if result['result']:
            msg = '表名修改成功'
        else:
            msg = '表名修改失败'
        return json.dumps({'msg': msg, 'is_success': result['result']})

    @staticmethod
    def alter_column_name(data):
        table_name, columns_info, values = data['table_name'], data['columns_info'], data['values']
        old_name_lst = []
        for item in columns_info:
            old_name_lst.append(item['COLUMN_NAME'])
            old_name_lst.append(item['COLUMN_COMMENT'])
        value_index = 0
        for info in columns_info[1:]:
            info['new_name'] = values[value_index]
            value_index = value_index + 1
            info['new_column_comment'] = values[value_index]
            value_index = value_index + 1
        base_str = """ALTER  TABLE `%table_name` change `%old_column`  
        `%new_column` %data_type  COMMENT '%new_comment'; """
        exe_result = True
        for info in columns_info[1:]:
            if info['COLUMN_NAME'] != info['new_name'] or info['COLUMN_COMMENT'] != info['new_column_comment']:
                new_str = base_str.replace('%table_name', DataFormat.table_name_format(table_name)) \
                    .replace('%old_column', info['COLUMN_NAME']).replace('%new_column', DataFormat.column_name_format(
                    info['new_name'])).replace('%new_comment', DataFormat.table_name_format(info['new_column_comment']))
                data_type = info['DATA_TYPE'].replace('多行文本', 'text').replace('文本', 'varchar(500)').replace(
                    '数字', 'decimal(15,4)').replace('日期', 'DATETIME')
                new_str = new_str.replace('%data_type', data_type)
                res = table_operator.alter_column_name_and_comment(new_str)
                if res is False:
                    exe_result = res
        if exe_result:
            return json.dumps({'msg': '修改成功', 'is_success': True})
        else:
            return json.dumps({'msg': '修改失败', 'is_success': False})

    @staticmethod
    def get_column_info(data):
        table_name = data['table_name']
        result = table_operator.get_column_info(table_name)
        for re in result:
            if re['DATA_TYPE'] == 'varchar':
                re['DATA_TYPE'] = '文本'
            elif re['DATA_TYPE'] == 'decimal':
                re['DATA_TYPE'] = '数字'
            elif re['DATA_TYPE'] == 'datetime':
                re['DATA_TYPE'] = '日期'
            elif re['DATA_TYPE'] == 'text':
                re['DATA_TYPE'] = '多行文本'
        return json.dumps({'msg': result, 'is_success': True})

    @staticmethod
    def add_column_name(data):
        """

        :param data:
        :return:
        """
        table_name, description, column_name, data_type = data['table_name'], \
                                                          data['description'], \
                                                          data['column_name'], \
                                                          data['type']
        column_name = DataFormat.column_name_format(column_name)
        description = DataFormat.column_name_format(description)
        table_name = DataFormat.table_name_format(table_name)
        base_str = ADD_COLUMN.replace('%table_name', table_name).replace('%column_name', column_name) \
            .replace('%new_comment', description)
        data_type = data_type.replace('number', 'decimal(15,4)').replace('date', 'DATETIME') \
            .replace('textarea', 'text')
        base_str = base_str.replace('%data_type', data_type).replace('text', 'varchar(500)')
        exe_result = table_operator.add_column(base_str)
        if exe_result:
            return json.dumps({'msg': '修改成功', 'is_success': True})
        else:
            return json.dumps({'msg': '修改失败', 'is_success': False})

    @staticmethod
    def delete_column(data):
        """

        :param data:
        :return:
        """
        table_name, column_name = data['table_name'], data['column_name']
        base_str = DELETE_COLUMN.replace('%table_name', table_name).replace('%column_name', column_name)
        exe_result = table_operator.add_column(base_str)
        if exe_result:
            return json.dumps({'msg': '删除成功', 'is_success': True})
        else:
            return json.dumps({'msg': '删除失败', 'is_success': False})

    @staticmethod
    def alter_table_info(change_info):
        """
        alter table info inference
        :param change_info:
        :return:
        """
        table_name_info = change_info['table_name']
        exe_res = []
        if table_name_info['is_change']:
            res = table_operator.alter_table_name(table_name_info['old_name'], table_name_info['new_name'])
            exe_res.append(res)
        for update_info in change_info['column_update_info']:
            data_type = TableInterface.change_data_type(update_info['type'])
            base_str = """ALTER  TABLE `%table_name` change `%old_column`  
                   `%new_column` %data_type  COMMENT '%new_comment'; """ \
                .replace('%table_name', DataFormat.table_name_format(table_name_info['new_name'])) \
                .replace('%old_column', update_info['old_column_name'])
            base_str = base_str.replace('%new_column', DataFormat.column_name_format(update_info['new_column_name'])) \
                .replace('%data_type', data_type).replace('%new_comment', update_info['description'])
            res = table_operator.alter_column_name_and_comment(base_str)
            exe_res.append(res)
        for add_info in change_info['column_add_info']:
            data_type = TableInterface.change_data_type(add_info['type'])
            description, column_name = add_info['description'], add_info['new_column_name']
            base_str = ADD_COLUMN.replace('%table_name',
                                          DataFormat.table_name_format(table_name_info['new_name'])).replace(
                '%column_name', DataFormat.column_name_format(column_name)) \
                .replace('%new_comment', description).replace('%data_type', data_type)
            exe_result = table_operator.add_column(base_str)
            exe_res.append(exe_result)
        for delete_info in change_info['column_delete_info']:
            res = table_operator.delete_column(table_name_info['new_name'], delete_info['COLUMN_NAME'])
            exe_res.append(res)
        table_operator.alter_table_comment(change_info['table_name']['new_name'], change_info['table_comment'])
        return json.dumps({'msg': str(exe_res), 'is_success': True})

    @staticmethod
    def change_data_type(type_str):
        """
        change data type
        :param type_str:
        :return:
        """
        if type_str == '多行文本':
            return 'text'
        if type_str == 'textarea':
            return 'text'
        type_str = type_str.replace('文本', 'varchar(500)').replace('数字', 'decimal(15,4)').replace('日期', 'DATETIME') \
            .replace('text', 'varchar(500)').replace('number', 'decimal(15,4)') \
            .replace('date', 'DATETIME')
        return type_str

    @staticmethod
    def delete_table(data):
        """
        delete table
        :param data:
        :return:
        """
        table_name = data['table_name']
        exe_result = table_operator.drop_table_by(table_name)
        if exe_result['result']:
            return json.dumps({'msg': '删除成功', 'is_success': True})
        else:
            return json.dumps({'msg': '删除失败', 'is_success': False})
