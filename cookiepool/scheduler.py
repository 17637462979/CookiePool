# -*- coding: utf-8 -*-
import time
from multiprocessing import Process
from .api import app
from .setting import *
from .creator import WeiboCookieCreator
from .tester import WeiboValidTester

class Scheduler(object):
    def api(self):
        print('API接口开始运行: ')
        app.run(host=API_HOST, port=API_PORT)

    def creater(self, cycle=CYCLE):
        while True:
            print('Cookie生成器开始运行：')
            try:
                for name, cls in GENERATOR_MAP.items():
                    creator = eval(cls+'(name="' + name + '")')
                    creator.run()
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    def tester(self, cycle=CYCLE):
        while True:
            print('Cookie测试器开始运行')
            try:
                for name, cls in TESTER_MAP.items():
                    tester = eval(cls + '(name="' + name + '")')
                    tester.run()
                    print('Cookie测试器运行完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)


    def run(self):
        if API_ENABLED:
            api_process = Process(target=self.api)
            api_process.start()

        if CREATOR_ENABLED:
            creator_process = Process(target=self.creater)
            creator_process.start()

        if TESTER_ENABLED:
            tester_process = Process(target=self.tester)
            tester_process.start()
