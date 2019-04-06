import time
from multiprocessing import Process
from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.my_api import app
from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.my_settings import *
from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.my_generator import *
from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.my_tester import *


class Scheduler:
    """调度类"""
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Cookies检测进程开始执行')
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('Cookies 检测完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while True:
            print('Cookies 生成进程开始执行')
            try:
                for website, cls in GENERATOR_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('Cookies 生成完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)

    @staticmethod
    def api():
        print('API 接口开始执行')
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        if API_PROCESS:
            api_process = Process(target=Scheduler.api)
            api_process.start()

        if GENERATOR_PROCESS:
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()

        if VALID_PROCESS:
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()