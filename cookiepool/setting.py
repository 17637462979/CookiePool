# -*- coding: utf-8 -*-

# API host and port
API_HOST = '127.0.0.1'
API_PORT = '8888'


# api、测试器、cookies生产器开关
API_ENABLED = True
CREATOR_ENABLED = True
TESTER_ENABLED = True

# 云打码的参数设置
YUNDAMA_USERNAME = 'vash1996'
YUNDAMA_PASSWORD = 'zhouxin'
YUNDAMA_APP_ID = '6272'
YUNDAMA_APP_KEY = '66e73c9d840f7121200c4a856167ce91'
YUNDAMA_API_URL = 'http://api.yundama.com/api.php'
YUNDAMA_MAX_RETRY = 20

# redis参数设置
REDIS_HOST = '127.0.0.1'
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
GENERATOR_MAP = {
    'weibo': 'WeiboCookieCreator'
}

# 测试类
TESTER_MAP = {
    'weibo': 'WeiboValidTester'
}


