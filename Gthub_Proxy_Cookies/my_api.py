import json
from flask import Flask, g
from study_crawler.Proxy_Cookies.my_settings import *

app = Flask(__name__)

@app.route('/')
def index():
    return '<h2>My Cookies Proxy</h2>'

def get_conn():
    for website in GENERATOR_MAP:
        if not hasattr(g, website):
            setattr(g, website + '_cookies', eval('RedisClient' + '("cookies", "' + website + '")'))
        return g

@app.route('/<website>/random')
def random(website):
    """获取随机的Cookies，访问地址如/weibo/random"""
    g = get_conn()
    cookies = getattr(g, website + '_cookies').random()
    return cookies
