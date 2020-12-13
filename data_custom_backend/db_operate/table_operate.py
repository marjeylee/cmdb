# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： table_operate
Description :
Author : 'li'
date： 2020/10/20
-------------------------------------------------
Change Activity:
2020/10/20:
-------------------------------------------------
"""
from config.database_config import *
from db_operate.data_format import DataFormat
from db_operate.sql_str import QUERY_TABLE_NAME, DROP_TABLE, ALERT_TABLE_NAME, CREATE_TABLE, QUERY_COLUMN_INFO, \
    DELETE_COLUMN, ALTER_TABLE_COMMENT
from llib.db_utility.mysql_relevant.connection_pool.db_pool import MysqlConnectionPool


class TableOperator:
    def __init__(self):
        self.pool = MysqlConnectionPool(host=DB_IP, user=DB_USER, passwd=DB_PASSWORD,
                                        db=DB_NAME, port=DB_PORT, charset='utf8')

    def query_table_name(self, query_name):
        """

        :param query_name:
        :return:
        """
        rows = self.pool.select(QUERY_TABLE_NAME)
        query_tables = []
        for row in rows:
            name = row['TABLE_NAME']
            if len(query_name) > 0:
                if query_name in name:
                    query_tables.append(row)
            else:
                query_tables.append(row)
        return query_tables

    def query_table_comment(self, query_name):
        """

        :param query_name:
        :return:
        """
        rows = self.pool.select(QUERY_TABLE_NAME)
        for row in rows:
            name = row['TABLE_NAME']
            if query_name == name:
                return row['TABLE_COMMENT']
        return ''

    def drop_table_by(self, table_name):
        """

        :param table_name:
        :return:
        """
        sql_str = DROP_TABLE.replace('$table_name', table_name)
        res = self.pool.execute_sql_str(sql_str)
        return res

    def alter_table_name(self, old_name, new_name):
        """

        :param new_name:
        :param old_name:
        :return:
        """
        new_name = new_name.replace(' ', '')
        new_name = DataFormat.table_name_format(new_name)
        sql_str = ALERT_TABLE_NAME.replace('%old_name', old_name).replace('%new_name', new_name)
        res = self.pool.execute_sql_str(sql_str)
        return res

    def get_column_info(self, table_name):
        """
        get column inf by table name
        :param table_name:
        :return:
        """
        sql_str = QUERY_COLUMN_INFO.replace('%table_name', table_name)
        res = self.pool.select(sql_str)
        return res

    def alter_column_name_and_comment(self, sql_str):
        """

        :param sql_str:
        :return:
        """
        res = self.pool.execute_sql_str(sql_str)
        return res['result']

    def add_column(self, sql_str):
        """

        :param sql_str:
        :return:
        """
        res = self.pool.execute_sql_str(sql_str)
        return res['result']

    def create_table_name(self, table_name, columns, table_comment):
        """

        :return:
        """
        table_name = DataFormat.table_name_format(table_name)
        table_comment = DataFormat.table_name_format(table_comment)
        sql_str = CREATE_TABLE.replace('%TABLE_NAME', table_name).replace('%table_comment', table_comment)
        columns_str = ''
        for column in columns:
            tmp_str = ''
            column_name = DataFormat.column_name_format(column['column_name'])
            description = DataFormat.column_name_format(column['description'])
            if column['type'] == 'text':
                tmp_str = '`' + column_name + '`' + ' varchar(500) COMMENT \'' + description + "'"
            elif column['type'] == 'date':
                tmp_str = '`' + column_name + '`' + ' DATETIME COMMENT \'' + description + "'"
            elif column['type'] == 'number':
                tmp_str = '`' + column_name + '`' + '  decimal(15,4) COMMENT \'' + description + "'"
            elif column['type'] == 'textarea':
                tmp_str = '`' + column_name + '`' + ' text COMMENT \'' + description + "'"
            columns_str = columns_str + tmp_str + ','
        columns_str = columns_str[:-1]
        sql_str = sql_str.replace('%COLUMNS_INFO', columns_str)
        res = self.pool.execute_sql_str(sql_str)
        return res['result']

    def delete_column(self, table_name, column_name):
        """

        :return:
        """
        base_str = DELETE_COLUMN.replace('%table_name', table_name).replace('%column_name', column_name)
        exe_result = self.add_column(base_str)
        return exe_result

    def alter_table_comment(self, table_name, table_comment):
        base_str = ALTER_TABLE_COMMENT.replace('%TABLE_NAME', table_name).replace('%TABLE_COMMENT', table_comment)
        exe_result = self.pool.execute_sql_str(base_str)
        return exe_result

    def delete_table(self, table_name):
        """

        :return:
        """
        base_str = DELETE_COLUMN.replace('%table_name', table_name)
        exe_result = self.add_column(base_str)
        return exe_result


def main():
    oper = TableOperator()
    res = oper.query_table_name('user')
    print(res)


if __name__ == '__main__':
    main()
