from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.my_settings import *
from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.my_db import RedisClient
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
import json
from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.Login.github import Login


class CookiesGenerator:
    """生成模块类"""
    def __init__(self, website=WEBSITE):
        """初始化，如果浏览器不使用，则设置为None"""
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)  # 首先创建一个Hash, {cookies:default}名字的格式
        self.accounts_db = RedisClient('accounts', self.website)  # 再创建一个Hash, {accounts:default}名字的格式
        self.init_browser()  # 启动selenium Chrome

    def __del__(self):
        self.close()   # 关闭 selenium

    def init_browser(self):
        """选择浏览器模拟登录"""
        if BROWSER_TYPE == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps[
                "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)
        elif BROWSER_TYPE == 'Chrome':  # 如果是 谷歌就创建 browser
            self.browser = webdriver.Chrome()
        elif BROWSER_TYPE == 'requests':
            pass


    def new_cookies(self, username, password):
        """新生成的Cookies,要用子类重新的"""
        raise NotImplementedError

    def process_cookies(self, cookies):
        """处理cookies"""
        dict = {}   # 创建一个字典
        for cookie in cookies:   # 将传进来的 cookies 一个一个
            dict[cookie['name']] = cookie['value']  # 将每一个cookies的name对应的值设为 key，每一个value对应的值设为 value
        return dict

    def run(self):
        """运行得到所有账户，然后顺次模拟登陆"""
        account_usernames = self.accounts_db.usernames()  # 获取accounts账户信息
        cookies_usernames = self.cookies_db.usernames()  # 获取cookies账户信息
        # 对比两个Hash 账户信息
        for username in account_usernames:  # 遍历 account所有的账户
            if not username in cookies_usernames:  # 如果cookies Hash里面没有
                password = self.accounts_db.get(username)  # 就获取它的账户对应的密码
                print('正在生产Cookies', '账号:', username, '密码:', password)
                result = self.new_cookies(username, password)  # 生产新的 cookies
                # 成功获取
                if result.get('status') == 1 and (BROWSER_TYPE == 'PhantomJS' or BROWSER_TYPE == 'Chrome'):
                    cookies = self.process_cookies(result.get('content'))  # 如果获取到了 cookies就处理它 {content：cookies}
                    print('成功获取到Cookies', cookies)
                    if self.cookies_db.set(username, json.dumps(cookies)):  # 保存到数据库获取到的cookies
                        print('成功保存Cookies')
                elif result.get('status') == 1 and BROWSER_TYPE == 'requests':
                    cookies = result.get('content')
                    print('成功获取到Cookies', cookies)
                    if self.cookies_db.set(username, json.dumps(cookies)):  # 保存到数据库获取到的cookies
                        print('成功保存Cookies')
                # 密码错误，移除账户
                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):  # 如果密码错误就删除账户
                        print('成功删除账户')
                else:
                    print(result.get('content'))
            else:
                print('所有账户都已经成功获取Cookies')

    def close(self):
        """关闭 browser"""
        if BROWSER_TYPE == 'requests':
            pass
        else:
            try:
                print('正在关闭 browser')
                self.browser.close()
                del self.browser
            except TypeError:
                print('browser 关闭失败')

class WeiboCookiesGenerator(CookiesGenerator):
    """继承上面的类"""
    def __init__(self, website=WEBSITE):
        CookiesGenerator.__init__(self, website)  # 继承父类的 __init__方法，并且重新website属性赋值
        self.website = website

    def new_cookies(self, username, password):
        """重写父类的new_cookies方法，生成Cookies"""
        # Login 为登录类，
        return Login(username, password).login()  # 传入账户密码登录，如果登录成功就返回1，不成功就2



