# API host and port
API_HOST = '127.0.0.1'
API_PORT = '8888'


# api、测试器、cookies生产器开关
API_ENABLED = True
CREATOR_ENABLED = True
TESTER_ENABLED = True

# 云打码的参数设置
# todo

# redis参数设置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None

REDIS_DOMAIN = '*'
REDIS_NAME = '*'

# 浏览器类型
DEFAULT_TYPE = 'Chrome'

# 产生器和验证器循环周期
CYCLE = 1800

# 用于生成cookie的线程数
THREAD_COUNT = 2

# 产生器类
GENERATO_MAP = {
    'weibo': 'WeiboCookieCreator'
}

# 测试类
TESTER_MAP = {
    'weibo': 'WeiboValidTester'
}


