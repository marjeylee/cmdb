# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     log_util
   Description :
   Author :       'li'
   date：          2020/3/30
-------------------------------------------------
   Change Activity:
                   2020/3/30:
-------------------------------------------------
"""
import datetime
import time

from llib.log_utility.time_format import TimeFormat
from llib.file_utility.file_path_utility import combine_file_path, create_dir

LOG_DIR = combine_file_path('log/')
create_dir(LOG_DIR)


def get_launch_time():
    return TimeFormat.date_stamp_to_datetime(time.time()).replace(' ', '.').replace(':', '-')


LAUNCH_TIME = get_launch_time()

LOG_TMP_PATH = 'log/log-%s.log' % LAUNCH_TIME
LOG_PATH = LOG_DIR = combine_file_path(LOG_TMP_PATH)


def get_current_time():
    """
    get current time
    :return:
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def __save_log_to_file(log_content):
    """
    save log to file
    :param log_content:
    :return:
    """
    with open(LOG_PATH, mode='a', encoding='utf8') as file:
        file.write(log_content + '\n')


def save_log(content, level='INFO'):
    """
    save log
    :param content:
    :param level: info  launch error
    :return:
    """
    current_time = get_current_time()
    log_content = current_time + ' [' + level + '] ' + content
    __save_log_to_file(log_content)
    print(log_content)


def main():
    log_info = 'dsadsad'
    level = 'INFO'
    save_log(content=log_info, level=level)


if __name__ == '__main__':
    main()
