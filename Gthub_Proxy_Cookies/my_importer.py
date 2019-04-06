from study_crawler.Proxy_Cookies.my_db import RedisClient

conn = RedisClient('accounts', 'github')

def set(account, sep=' '):
    """录入账户密码的函数，如果redis库中已经存在就不需要再次输入，否则会录入失败"""
    username, password = account.split(sep)
    result = conn.set(username, password)
    print('账号', username, '密码', password)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入账号密码组, 输入exit退出读入')
    print('请勿重复输入')
    while True:
        account = input()
        if account == 'exit':
            break
        set(account)


if __name__ == '__main__':
    scan()