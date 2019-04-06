import requests
from lxml import etree


class Login:
    def __init__(self, account, password):
        self.headers = {
            'Referer': 'https://github.com/login',
            'Host': 'github.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
        }
        self.account = account
        self.password = password
        self.login_url = 'https://github.com/login'  # 登陆网页
        self.post_url = 'https://github.com/session'  # 不输入账号密码点登陆网页
        self.logined_url = 'https://github.com/settings/profile'  # 登录后的个人详情页面
        self.session = requests.Session()   # 最重要的步骤,Session 可以帮我们维持一个会话,而且可以自动处理Cookies,不用去担心Cookies 问题

    def token(self):
        '''
        解析出token
        :return:
        '''
        response = self.session.get(self.login_url, headers=self.headers)  # 在session页面获取到 authenticity_token
        selector = etree.HTML(response.text)
        token = selector.xpath('//div//input[2]/@value')[0]
        return token

    def login(self):
        '''
        模拟登陆
        :param email:
        :param password:
        :return:
        '''
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': self.account,
            'password': self.password
        }
        self.session.post(self.post_url, data=post_data, headers=self.headers)  # post 登陆账户密码
        res = self.session.get(self.logined_url, headers=self.headers)
        r = res.cookies.get_dict()
        if r:
            return {
                'status': 1,
                'content': r
            }
        else:
            pass

