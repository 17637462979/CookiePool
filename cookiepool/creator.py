class CookieCreator(object):
    def __init__(self, name='default'):
        self.name = name
        self.account_redis = AccountRedisClient(name=self.name)
        self.cookie_redis = CookieRedisClient(name=self.name)

    def run(self):
        # Todo

class WeiboCookieCreator(CookieCreator):
    def __init__(self, name='weibo'):
        super().__init__(name=name)