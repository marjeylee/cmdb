# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： data_format
Description :
Author : 'li'
date： 2020/10/26
-------------------------------------------------
Change Activity:
2020/10/26:
-------------------------------------------------
"""


class DataFormat:
    @staticmethod
    def table_name_format(original_name):
        """
        table_name format
        :param original_name:
        :return:
        """
        original_name = original_name.replace('@', '').replace('#', '').replace('￥', '').replace('$', '') \
            .replace('%', '').replace('^', '').replace('&', '').replace('*', '') \
            .replace('(', '（').replace(')', '）').replace('[', '【').replace(']', '】') \
            .replace(':', '：').replace(';', '；').replace(',', '，').replace('.', '。') \
            .replace('？', '').replace('\'', '’').replace('"', '“').replace('~', '') \
            .replace('`', '').replace('+', '').replace('{', '').replace('}', '').replace('!', '') \
            .replace('<', '《').replace('>', '》').replace(' ', '').replace('\'', '') \
            .replace('=', '').replace('/', '').replace('?', '').replace('\\', '')
        return original_name

    @staticmethod
    def data_value_format(original_name):
        return original_name.replace("'", "\\\'")

    @staticmethod
    def column_name_format(original_name):
        original_name = original_name.replace('@', '').replace('#', '').replace('￥', '').replace('$', '') \
            .replace('%', '').replace('^', '').replace('&', '').replace('*', '') \
            .replace('(', '（').replace(')', '）').replace('[', '【').replace(']', '】') \
            .replace(':', '：').replace(';', '；').replace(',', '，').replace('.', '。') \
            .replace('？', '').replace('\'', '’').replace('"', '“').replace('~', '') \
            .replace('`', '').replace('+', '').replace('{', '').replace('}', '').replace('!', '') \
            .replace('<', '《').replace('>', '》').replace(' ', '').replace('\'', '') \
            .replace('=', '').replace('/', '').replace('?', '').replace('\\', '')
        return original_name
