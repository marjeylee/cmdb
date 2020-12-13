# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： gen_sql_str
Description :
Author : 'li'
date： 2020/11/4
-------------------------------------------------
Change Activity:
2020/11/4:
-------------------------------------------------
"""
import os

from db_operate.data_format import DataFormat
from llib.file_utility.csv_utility import csv_file_to_mapping
from llib.file_utility.xls_utility import read_xls_content_to_mapping


def _get_create_table_sql(param, table_name):
    base_sql = """create table `%table_name` ( unique_id int(4) primary key not null auto_increment,%column_info);"""
    combine_sql = ''
    for key in param:
        data_type = param[key]
        key = DataFormat.column_name_format(key)
        sql = '`' + key + '` ' + data_type + ' ,'
        combine_sql = combine_sql + sql
    base_sql = base_sql.replace('%table_name', table_name).replace('%column_info', combine_sql[:-1])
    return base_sql


def _get_insert_sql_list(content_mapping, name):
    insert_list = []
    for row in content_mapping[1:]:
        insert_sql = """insert into `%table_name` (%column_names) values (%values);""".replace('%table_name', name)
        column_names = ''
        values = ''
        has_content = False
        for key in row:
            value = row[key]
            if len(str(value)) > 0:
                has_content = True
            if key == '日期':
                value = value.replace('年', '-').replace('月', '-').replace('日', ' ') + '00:00:00'
            key = DataFormat.column_name_format(key)
            column_names = column_names + '`' + key + '`,'

            values = values + '\'' + str(value) + '\','
        column_names = column_names[:-1]
        values = values[:-1]
        if not has_content:
            continue
        insert_sql = insert_sql.replace('%column_names', column_names).replace('%values', values)
        insert_list.append(insert_sql)
    return insert_list


def main():
    csv_path = 'C:/Users/Administrator/Desktop/专线外联监控地址.xlsx'
    # content_mapping = csv_file_to_mapping(csv_path)
    content_mapping = read_xls_content_to_mapping(csv_path)
    name = os.path.split(csv_path)[1].split('.')[0]
    create_table_sql = _get_create_table_sql(content_mapping[0], name)
    insert_sql_list = _get_insert_sql_list(content_mapping, name)
    print(create_table_sql)
    for sql in insert_sql_list:
        print(sql)


if __name__ == '__main__':
    main()
