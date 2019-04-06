from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.my_settings import *
from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.my_db import RedisClient
import json
import requests


class ValidTester:
    """检测模块"""
    def __init__(self, website=WEBSITE):
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)  # 依然是这个两个Hash
        self.accounts_db = RedisClient('accounts', self.website)

    def test(self, username, cookies):
        """子类重写"""
        raise NotImplementedError

    def run(self):
        cookies_groups = self.cookies_db.all()  # 获取所有的账户和Cookies
        for username, cookies in cookies_groups.items():  # 遍历账户和Cookies组成的字典
            self.test(username, cookies)

class WeiboValidTester(ValidTester):
    """继承上面的父类"""
    def __init__(self, website=WEBSITE):
        ValidTester.__init__(self, website)  # 继承父类的__init__方法

    def test(self, username, cookies):
        """重写父类的test方法，检测Cookies可以的方法"""
        print('正在测试Cookies', '用户名:', username)
        try:
            cookies = json.loads(cookies)  # loads将文本转换成json对象
        except TypeError:
            print('Cookies 不合法', username)
            self.cookies_db.delete(username)  # 那就在cookies 的hash里面删除这个账户
            print('删除cookies', username)
        try:
            test_url = TEST_URL_MAP[self.website]  # 这是个字典名称对应网址，选取微博网址
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)  # allow_redirects禁止重定向
            if response.status_code == 200:  # 有效的就不用管
                print('Cookies有效', username)
                # print('部分测试结束', response.text[0:50])
            else:
                print(response.status_code, response.headers)
                print('Cookies 失效', username)
                self.cookies_db.delete(username)  # 无效的cookies就删除
                print('删除Cookies', username)
        except ChildProcessError as e:
            print('发生异常', e.args)

