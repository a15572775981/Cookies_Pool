# 配置文件
# 存储模块
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
# 调度模块
# 产生器和验证器循环周期
CYCLE = 120

# 以下需要自己修改
########################################################################################################################

# 生成模块
BROWSER_TYPE = 'requests'  # 这里是配置selenium，如果是谷歌就填 Chrome，如果是requests就填requests

# 检测模块，自己配置得到cookies后，需要检查cookies是否可用的网址
TEST_URL_MAP = {
    'github': 'https://github.com/'
}
# 生成cookies类，key是你目标网址的名称，名称自己起， 后面是生成类，不需修改
GENERATOR_MAP = {
    'github': 'WeiboCookiesGenerator'
}

# 测试类，key是你目标网址的名称，名称自己起， 后面是测试类，不需修改
TESTER_MAP = {
    'github': 'WeiboValidTester'
}

# API地址和端口， 如果 API_PROCESS = False,那么就不用管它，
API_HOST = 'localhost'
API_PORT = 9999

# 进程开关，想开那个开那个
# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器开关，循环检测数据库中Cookies是否可用
VALID_PROCESS = True
# API接口服务，如果False需要去 use_cookies_api文件夹中get_redis_db.py 中的方法，该方法是直接从redis获取随机cookies的方法
API_PROCESS = False

# redis上cookies对应的名称
WEBSITE = 'github'