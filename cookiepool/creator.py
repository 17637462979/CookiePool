# -*- coding: utf-8 -*-
import json
import queue
from queue import Queue
from threading import Thread

import requests

from .db import AccoutRedisClient, CookieRedisClient
from .setting import *
from .yundama import Yundama
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import  WebDriverWait




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
        print("WeiboCookieCreator start")
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
        self.ydm = Yundama(YUNDAMA_USERNAME,
                           YUNDAMA_PASSWORD,
                           YUNDAMA_APP_ID,
                           YUNDAMA_APP_KEY)

    def _init_browser(self, browser_type):
        if browser_type == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh;Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS(desired_capabilities=caps)
            self.browser.set_window_size(1400, 500)
        elif browser_type == 'Chrome':
            opt = webdriver.ChromeOptions()
            opt.headless = True
            path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            self.browser = webdriver.Chrome(executable_path=path, options=opt)
            self.browser.set_window_size(1400, 500)

    def is_success(self, username):
        wait = WebDriverWait(self.browser, 12)
        success = wait.until(EC.visibility_of_element_located((By.XPATH, '//textarea[@class="W_input"]')))
        if success:
            print('登录成功')
        cookies = {}
        for cookie in self.browser.get_cookies():
            if cookie['name'] == 'SUB':
                cookies[cookie['name']] = cookie["value"]
        print("成功获取到Cookies")
        return (username, json.dumps(cookies))

    def new_cookies(self, username, password):
        print('为{}创建cookie').format(username)
        self.browser.delete_all_cookies()
        self.browser.get('https://weibo.com/')
        wait = WebDriverWait(self.browser, 25)

        try:
            user = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                '//input[@id="loginname"]')))
            user.send_keys(username)

            psd = wait.until(EC.visibility_of_element_located((By.XPATH, '//iinput[@type="password"]')))
            psd.send_keys(password)
            btn = wait.until(EC.visibility_of_element_located((By.XPATH, '//a[@tabindex="6"')))
            btn.click()
            try:
                result = self.is_success(username)
                if result:
                    return result
            except TimeoutException:
                print('出现验证码，开始识别验证码')
                yzm = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="verifycode"]')))
                code = self.browser.find_element_by_xpath(('//img[@node-type="verifycode_image"]'))
                code_url = code.get_attribute('src')
                response = requests.get('src')
                res = self.ydm.identify(stream=response.content)
                if not res:
                    print('验证码识别失败， 跳过识别')
                    return
                yzm.send_keys(res)
                btn.click()
                try:
                    result = self.is_success(username)
                    if result:
                        return result
                except TimeoutException:
                    url = self.browser.current_url
                    if 'https://security.weibo.com/captcha' in url:
                        print("账号异常，删除账号!")
                        self.account_redis.delete(username)
                    else:
                        print('已超时，请下次再试！')
        except WebDriverException as e:
            print(e.args)

    def run(self):
        while True:
            if self.queue.empty():
                break
            account = self.queue.get()
            self._init_browser(browser_type=DEFAULT_TYPE)
            results = self.new_cookies(account.get('username'), account.get('password'))
            self.cloe()
            if results:
                username, cookies = results
                print('aving cookies to redis', username, cookies)
                self.cookie_redis.set(username, cookies)

    def close(self):
        try:
            print('关闭浏览器')
            self.browser.close()
            del self.browser
        except TypeError:
            print('浏览器未关闭')

