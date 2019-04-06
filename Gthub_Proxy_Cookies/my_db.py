import random
import redis
from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.my_settings import *

class RedisClient:
    """存储类"""
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """连接信息"""
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """创建 Hash 名称"""
        return "{type}:{website}".format(type=self.type, website=self.website)  # 创建Hash名称，名称以字典形式，参数是要传入的自己起的名字

    def set(self, username, value):
        """设置键值对"""
        return self.db.hset(self.name(), username, value)  # 想自己起的Hash里面添加账户和密码的键值对

    def get(self, username):
        """根据键名获取键值"""
        return self.db.hget(self.name(), username)  # 根据这 Hash名称里面的 username 得到 username对应的value

    def delete(self, username):
        """根据键名删除键值对"""
        return self.db.hdel(self.name(), username)  # 根据这 Hash名称里面的 username 删除这个键值对

    def count(self):
        """获取数目"""
        return self.db.hlen(self.name())  # 根据名称获取数量

    def random(self):
        """随机得到键值"""
        return random.choice(self.db.hvals(self.name()))  # hvals:获取名称的所有键值对

    def usernames(self):
        """获取所有用户信息"""
        return self.db.hkeys(self.name())  # 获取键名，这里指账户

    def all(self):
        """获取所有键值对"""
        return self.db.hgetall(self.name())  # 获取所有键值对

