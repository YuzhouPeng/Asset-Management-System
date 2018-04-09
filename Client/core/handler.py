#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import time
import urllib.parse
import urllib.request
from core import info_collection
from conf import settings


class ArgvHandler(object):

    def __init__(self, args):
        self.args = args
        self.parse_args()

    def parse_args(self):
        """
        Analyze parameter
        :return:
        """
        if len(self.args) > 1 and hasattr(self, self.args[1]):
            func = getattr(self, self.args[1])
            func()
        else:
            self.help_msg()

    @staticmethod
    def help_msg():
        """
        Help instruction
        :return:
        """
        msg = '''
        collect_data        收集硬件信息
        report_data         收集硬件信息并汇报
        '''
        print(msg)

    @staticmethod
    def collect_data():
        """Collecting hardware information for testing"""
        info = info_collection.InfoCollection()
        asset_data = info.collect()
        print(asset_data)

    @staticmethod
    def report_data():
        """
        Collection hardware information and send it to server
        :return:
        """
        # Collecting information
        info = info_collection.InfoCollection()
        asset_data = info.collect()
        # Packing data to a dictionary and convert to json format
        data = {"asset_data": json.dumps(asset_data)}
        # Forming url based on the configuration in setting.py
        url = "http://%s:%s%s" % (settings.Params['server'], settings.Params['port'], settings.Params['url'])
        print('正在将数据发送至： [%s]  ......' % url)
        try:
            # Sending post request by using build-in urllib.request library
            # 需要先将数据进行封装，并转换成bytes类型
            data_encode = urllib.parse.urlencode(data).encode()
            response = urllib.request.urlopen(url=url, data=data_encode, timeout=settings.Params['request_timeout'])
            print("\033[31;1m发送完毕！\033[0m ")
            message = response.read().decode()
            print("返回结果：%s" % message)
        except Exception as e:
            message = "发送失败"
            print("\033[31;1m发送失败，%s\033[0m" % e)
        # 记录发送日志
        with open(settings.PATH, 'ab') as f:
            string = '发送时间：%s \t 服务器地址：%s \t 返回结果：%s \n' % (time.strftime('%Y-%m-%d %H:%M:%S'), url, message)
            f.write(string.encode())
            print("日志记录成功！")