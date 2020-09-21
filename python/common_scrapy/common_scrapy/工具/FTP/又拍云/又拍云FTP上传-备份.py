# _*_ coding:utf-8 _*_


import paramiko
from ScrapyMongoDBForSearch.settings import FTP_HOST, FTP_PORT, FTP_USERNAME, FTP_PASSWORD, FTP_REMOTE_PATH


class DoFTP():
    '''
    FTP 上传操作
    '''

    def __init__(self):
        self.host = FTP_HOST
        self.port = FTP_PORT
        self.username = FTP_USERNAME
        self.password = FTP_PASSWORD
        self.remote_path = FTP_REMOTE_PATH

    def login(self):
        '''
        登录 FTP 操作
        :return:
        '''
        self.transport = paramiko.Transport((self.host, self.port))
        # Exception: Error reading SSH protocol banner[WinError 10054] 远程主机强迫关闭了一个现有的连接。
        # 需要设置 banner_timeout 的值，默认值为 15s，现在修改为 60s，但是不起作用
        # self.transport.banner_timeout = 60
        self.transport.banner_timeout = 300
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def logout(self):
        '''
        退出 FTP 操作
        :return:
        '''
        self.sftp.close()
        self.transport.close()

    def uploads(self, local_path, remote_path, file_name):
        '''
        文件上传操作
        :param local_path: 本地路径 'C:/Users/shanhai/Desktop/DoSFTP/'
        :param remote_path:  远程路径 '/zls/server/apache/htdocs/ZlsLhx_BD__ZhiZhu/Uploads/Imgs/'
        :param file_name:  上传文件的文件名 'uploads.txt'
        :return:
        '''
        result = ""
        try:
            self.login()
            result = self.sftp.put(local_path + file_name, remote_path + file_name)
        except IOError:
            err_str_len = self.getSSH(remote_path)
            if err_str_len == 0:
                result = self.sftp.put(local_path + file_name, remote_path + file_name)
        finally:
            self.logout()
            if result:
                return True
            else:
                return False

    def getSSH(self, remote_path):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, port=self.port, username=self.username, password=self.password, compress=True)
        tdin, stdout, stderr = ssh.exec_command('mkdir -p ' + remote_path)
        err_str_len = len(stderr.read())  # 计算错误信息的长度，如果长度为零，说明没有错误信息，也就是多级目录创建成功！
        ssh.close()
        return err_str_len


if __name__ == '__main__':
    doftp = DoFTP()
    local_path = 'C:/Users/shanhai/Desktop/'
    remote_path = '/zls/server/apache/htdocs/ZlsLhx_BD__ZhiZhu/zo/gnweo/gnweo/Imgs/345/'
    file_name = 'uploads.txt'
    doftp.uploads(local_path, remote_path, file_name)
