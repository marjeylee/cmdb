# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     telnet_client
   Description :
   Author :       'li'
   date：          2019/12/31
-------------------------------------------------
   Change Activity:
                   2019/12/31:
-------------------------------------------------
"""
import telnetlib
import time

from llib.connect_utility.connector_interface import ConnectorInterface
from llib.connect_utility.error_byte_fiter import ERROR_BYTE_FILTER
from llib.log_utility.log_util import save_log


class TelnetClient(ConnectorInterface):
    def __init__(self, host_ip, user_name, password):
        self.host_ip = host_ip
        self.user_name = user_name
        self.password = password
        self.is_connection = None
        self.connection = self.tn

    def close(self):
        self.tn.close()
        save_log('关闭%s连接' % self.host_ip, 'INFO')

    def __create_connection(self):
        """
        create telnet connection
        :return:
        """
        try:
            self.tn = telnetlib.Telnet()
            self.tn.open(self.host_ip, port=23)

            self.tn.read_until(self.command_template.login_username_end_print.encode('ascii'), timeout=2)
            self.tn.write(self.user_name.encode('ascii') + b'\n')
            self.tn.read_until(self.command_template.login_password_end_print.encode('ascii'), timeout=2)
            self.tn.write(self.password.encode('ascii') + b'\n')
            is_login_success = self.__check_is_login_success()
            return is_login_success
        except:
            save_log(content='telnet 登录%s失败' % self.host_ip, level='ERROR')
            return False

    def __fetch_execute_result(self):
        """
        fetch execute result
        :return:
        """
        time.sleep(1)
        byte_result = self.tn.read_very_eager()
        exe_result = ERROR_BYTE_FILTER.filter_error_bytes(byte_result)
        return exe_result

    def execute_command(self, command, is_read_first_page=False):
        """
        execute command
        :param is_read_first_page:
        :param command:
        :return:
        """
        if self.is_connection is False:
            save_log('telnet登录失败，不能执行命令')
            return None
        self.tn.write(command.encode('ascii') + b'\r\n')
        command_result = self.__fetch_execute_result()
        all_result = command_result
        if not is_read_first_page:  # only read first page
            while True:
                self.tn.write(' '.encode('ascii') + b'\r\n')
                command_result = self.__fetch_execute_result()
                filter_command = command_result.replace('\r\n', '').replace(' ', '')

                all_result = all_result + command_result
                # print(command_result)
                if len(filter_command) == 0 or filter_command[-1] in '>#':
                    break
        all_result = self.__exe_space_one_more_time(all_result)
        # save_log(all_result)
        return all_result

    def __input_blank_space(self):
        self.tn.write(' '.encode('ascii') + b'\r\n')
        time.sleep(1)
        command_result = self.__fetch_execute_result()
        return command_result

    def __check_is_login_success(self):
        """
        check is login success
        :return:
        """
        command_result = self.__input_blank_space().strip()
        if len(command_result) > 0 and (command_result[-1] in '#>'):
            save_log(content='telnet 登录%s 成功' % self.host_ip, level='INFO')
            return True
        else:
            command_result = self.__input_blank_space().strip()
        if len(command_result) > 0 and (command_result[-1] in '#>'):
            save_log(content='telnet 登录%s 成功' % self.host_ip, level='INFO')
            return True
        save_log(content='telnet 登录%s 失败' % self.host_ip, level='ERROR')
        return False

    def __exe_space_one_more_time(self, all_result):
        """
        :param all_result:
        :return:
        """
        all_result = all_result + '\n'
        self.tn.write(' '.encode('ascii') + b'\r\n')
        more_result = self.__fetch_execute_result()
        exe_result = all_result + more_result
        return exe_result


def main():
    telnet_client = TelnetClient('100.100.253.128', 'ciscoAdmin', 'IGGv1wG4E2jZ', H3CDefaultCommandTemplate())
    telnet_client.close()


if __name__ == '__main__':
    main()
