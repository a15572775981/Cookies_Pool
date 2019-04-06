from study_crawler.Github_Cookies_Pool.Gthub_Proxy_Cookies.my_scheduler import Scheduler

def run():
    """启动代理cookies入口"""
    s = Scheduler()
    s.run()

if __name__ == '__main__':
    run()