# -*- coding: utf-8 -*-
"""
-------------------------------------------------
File Name： get
Description :
Author : 'li'
date： 2020/11/9
-------------------------------------------------
Change Activity:
2020/11/9:
-------------------------------------------------
"""
from llib.file_utility.csv_utility import csv_file_to_mapping
from llib.file_utility.xls_utility import read_xls_content_to_mapping


def main():
    mapping = csv_file_to_mapping('分支行.csv')
    for item in mapping:
        res = item['网点业务YW']
        print(res)


if __name__ == '__main__':
    main()
