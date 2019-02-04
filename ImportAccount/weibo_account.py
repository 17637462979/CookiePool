import redis


db = redis.StrictRedis()
KEY = "account:weibo"

with open('./ImportAccount/weibo_account.txt', encoding='utf-8') as f:
    for line in f:
        line = line.strip('\n')
        k, v = line.split('----')
        db.set(KEY + ':' + k, v)
