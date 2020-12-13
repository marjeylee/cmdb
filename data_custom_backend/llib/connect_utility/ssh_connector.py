import time

import paramiko

from llib.connect_utility.connector_interface import ConnectorInterface
from llib.connect_utility.error_byte_fiter import ERROR_BYTE_FILTER
from llib.log_utility.log_util import save_log


class SSHConnector(ConnectorInterface):
    def __init__(self, host_ip, user_name, password):
        """
        init method
        """
        self.host_ip = host_ip
        self.user_name = user_name
        self.password = password
        self.is_connected = False
        self.connection = None
        self.channel = None
        self._connection()

    def _connection(self):
        """
        get connection
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            save_log('尝试登录SSH，IP: %s' % self.host_ip, 'INFO')
            ssh.connect(self.host_ip, 22, self.user_name, self.password, timeout=10)
            if ssh is not None:
                save_log('SSH登录IP:%s成功' % self.host_ip, 'INFO')
                self.connection = ssh
                self.channel = self.connection.invoke_shell()
                self.is_connected = True
                self.__fetch_execute_result(self.channel)
                return
            save_log('SSH登录IP:%s失败' % self.host_ip, 'ERROR')
            self.connection = None
        except:
            save_log('SSH登录IP:%s失败' % self.host_ip, 'ERROR')
            self.connection = None

    def close(self):
        try:
            self.connection.close()
            self.channel.close()
            save_log('关闭%s连接' % self.host_ip, 'INFO')
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def __fetch_execute_result(channel):
        """
        fetch execute result
        :param channel:
        :return:
        """
        time.sleep(0.5)
        exe_result = ''
        while channel.recv_ready():
            lines = channel.recv(1024)
            lines = lines.decode('utf8')
            lines = ERROR_BYTE_FILTER.filter_error_bytes(lines)
            exe_result = exe_result + lines
        return exe_result

    def execute_command(self, command, is_read_first_page=True):
        """
        execute command
        :param is_read_first_page:
        :param command:
        :return:
        """
        if self.connection is None:
            save_log('IP:%s,SSH登录失败,不能执行命令' % self.host_ip, 'ERROR')
            return None
        time.sleep(0.2)
        _ = self.__fetch_execute_result(self.channel)
        self.channel.send(command + '\r')
        time.sleep(2)
        exe_result = ''
        while True:
            res = self.__fetch_execute_result(self.channel)
            if len(res) == 0:
                break
            exe_result = exe_result + res
        time.sleep(0.2)
        if is_read_first_page:
            self.channel.send('\t')
            time.sleep(0.2)
            _ = self.__fetch_execute_result(self.channel)
        else:
            while True:
                if not self.check_is_output_finish(exe_result):
                    exe_result = exe_result + '\n'
                    self.channel.send(' ')
                    more_result = self.__fetch_execute_result(self.channel)
                    exe_result = exe_result + more_result
                else:
                    break
        # exe_result = self.__exe_space_one_more_time(exe_result)
        return exe_result

    def __exe_space_one_more_time(self, exe_result):

        """
        :param exe_result:
        :return:
        """
        exe_result = exe_result + '\n'
        self.channel.send(' ')
        self.channel.send('\r\n')
        more_result = self.__fetch_execute_result(self.channel)
        exe_result = exe_result + more_result
        return exe_result

    @staticmethod
    def check_is_output_finish(exe_result):
        """

        :param exe_result:
        :return:
        """
        tmp_str = exe_result.replace(' ', '').replace('\r', '').replace('\n', '')
        if len(tmp_str) == 0 or tmp_str[-1] in '#>':
            return True
        return False
