from queue import Queue
from threading import Thread
from .db import AccoutRedisClient, CookieRedisClient
from .setting import *


class CookieCreator(object):
    def __init__(self, name='default'):
        self.name = name
        self.account_redis = AccoutRedisClient(name=self.name)
        self.cookie_redis = CookieRedisClient(name=self.name)

    def set_cookies(self):
        for i in range(THREAD_COUNT):
            cookieThread = CookieCreatorThread(queue,
                                               cookie_redis=self.cookie_redis,
                                               account_redis=self.account_redis)
            cookieThread.start()

    def run(self):
        accounts = self.account_redis.all()
        cookies = self.cookie_redis.all()
        accounts = list(accounts)
        valid_users = [cookie.get('username') for cookie in cookies]
        print('从数据库中获取： {}个账号，{}个cookie'.format(len(accounts), len(valid_users)))
        count = len(accounts) - len(valid_users)
        if count:
            queue = Queue(count)
            for account in accounts:
                if not account.get('username') in valid_users:
                    queue.put(account)
            self.set_cookies(queue)


class WeiboCookieCreator(CookieCreator):
    def __init__(self, name='weibo'):
        super().__init__(name=name)


class CookieCreatorThread(Thread):
    def __init__(self, queue, cookie_redis, account_redis, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.cookie_redis = cookie_redis
        self.account_redis = account_redis
        self.ydm = Yundame() # todo
