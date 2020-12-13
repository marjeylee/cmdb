# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： download_inference
Description :
Author : 'li'
date： 2020/10/28
-------------------------------------------------
Change Activity:
2020/10/28:
-------------------------------------------------
"""
import json

from db_operate.data_operate import DataOperator
from llib.file_utility.xls_utility import write_xls_content
from llib.log_utility.debug_log_util import get_current_time

data_operator = DataOperator()


class DownloadInference:
    @staticmethod
    def gen_excel(query_parameter):
        """

        :param query_parameter:
        :return:
        """
        res = data_operator.query_data(query_parameter)
        if len(res) == 0:
            return None
        keys = list(res[0].keys())
        format_rows = [keys]
        for row in res:
            new_row = []
            for k in keys:
                v = row[k]
                new_row.append(v)
            format_rows.append(new_row)
        file_name = 'export' + '_' + get_current_time(). \
            replace(':', ';').replace(' ', '_') + '.xls'
        write_xls_content(file_name, format_rows)
        return json.dumps({'msg': file_name, 'is_success': True})
