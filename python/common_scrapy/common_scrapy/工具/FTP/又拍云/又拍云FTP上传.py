# _*_ coding:utf-8 _*_


import upyun
from upyun import FileStore
from upyun import print_reporter


class DoFTP():
    '''
    FTP 上传操作
    '''

    def __init__(self):
        pass

    def uploads(self, local_path, remote_path, file_name, service):
        up = upyun.UpYun(service, 'lhx4xmupy', '6WQH73rdWIVJ732psGD3o4V4kl4pn1MO', timeout=30,
                         endpoint=upyun.ED_AUTO)
        local_file = local_path + file_name
        remote_file = remote_path + file_name
        # print(local_file)
        # print(remote_file)
        result = False
        with open(local_file, 'rb') as f:
            res = up.put(remote_file, f, checksum=False)
            if int(res.get('content-length')) > 0:
                result = True
        return result
        # result = up.put(remote_path + file_name, f, checksum=True,
        #                 need_resume=True, headers={'X-Upyun-Multi-Type': 'image/png'},
        #                 store=FileStore(), reporter=print_reporter)


if __name__ == '__main__':
    doftp = DoFTP()
    local_path = 'C:/Users/shanhai/Desktop/'
    remote_path = '/zls/server/apache/htdocs/ZlsLhx_BD__ZhiZhu/zo/gnweo/gnweo/Imgs/345/'
    file_name = 'uploads.txt'
    service = ''
    doftp.uploads(local_path, remote_path, file_name, service)
