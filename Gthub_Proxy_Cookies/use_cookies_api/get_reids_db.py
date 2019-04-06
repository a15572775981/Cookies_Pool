import random
import redis

# 获取随机Cookies方法

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None

HASH_NAME = 'cookies:自己的hash名称'  # 类似于cookies:github,
HASH_USER = 'hash自己的账户'

def get_randome_cookies():
    """根据键名获取键值"""
    cookies_list = []
    db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
    cookies = db.hgetall(HASH_NAME)
    for c in cookies:
        cookies_list.append(c)
    r = random.choice(cookies_list)
    return r

