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
        self.is_connected = None
        self.tn = None
        self.connection = self.tn
        self._create_connection()

    def close(self):
        self.tn.close()
        save_log('关闭%s连接' % self.host_ip, 'INFO')

    def _create_connection(self):
        """
        create telnet connection
        :return:
        """
        try:
            self.tn = telnetlib.Telnet()
            self.tn.open(self.host_ip, port=23)
            _ = self.read_all_content()
            _ = self.read_all_content()
            self.tn.write(self.user_name.encode('ascii') + b'\n')
            _ = self.read_all_content()
            _ = self.read_all_content()
            self.tn.write(self.password.encode('ascii') + b'\n')
            _ = self.read_all_content()
            _ = self.read_all_content()
            self.is_connected = self.__check_is_login_success()
            if self.is_connected:
                save_log(content='telnet 登录%s成功' % self.host_ip, level='INFO')
            else:
                save_log(content='telnet 登录%s失败' % self.host_ip, level='ERROR')
        except Exception as e:
            print(e)
            save_log(content='telnet 登录%s失败' % self.host_ip, level='ERROR')

    def __fetch_execute_result(self):
        """
        fetch execute result
        :return:
        """
        res = self.read_all_content()
        res_1 = self.read_all_content()
        res = res + res_1
        exe_result = ERROR_BYTE_FILTER.filter_error_bytes(res)
        return exe_result

    def execute_command(self, command, is_read_first_page=True):
        """
        execute command
        :param is_read_first_page:
        :param command:
        :return:
        """
        _ = self.read_all_content()
        if self.is_connected is False:
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
                if len(filter_command) == 0 or filter_command[-1] in '>#':
                    break
        # all_result = self.__exe_space_one_more_time(all_result)
        return all_result

    def __input_blank_space(self):
        self.tn.write(' '.encode('ascii') + b'\r\n')
        command_result = self.__fetch_execute_result()
        return command_result

    def __check_is_login_success(self):
        """
        check is login success
        :return:
        """
        for i in range(3):
            command_result = self.__input_blank_space().strip()
            if len(command_result) > 0 and (command_result[-1] in '#>'):
                return True
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

    def read_all_content(self):
        """
        read all content
        """
        time.sleep(0.5)
        content = ''
        for i in range(20):
            time.sleep(0.5)
            res_byte = self.tn.read_very_eager()
            if len(res_byte) == 0:
                # print(content)
                return content
            res_byte = res_byte.decode('utf8')
            content = content + res_byte
            # print(content)
        return content


def main():
    telnet_client = TelnetClient('100.100.253.128', 'ciscoAdmin', 'IGGv1wG4E2jZ')
    telnet_client.close()


if __name__ == '__main__':
    main()
