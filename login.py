# -*- coding: utf-8 -*-
import time
import sys
import re
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from PIL import Image


def login():

    username = '18811029214'
    passwd = 'xyf15038140312'

    driver = webdriver.Chrome(executable_path='/Users/uni/chromedriver')
    driver.get(
        'https://passport.58.com/login')
    time.sleep(1)

    pwdLogin = driver.find_element_by_id('pwdLogin')
    pwdLogin.click()

    # 输入用户名
    usernameUser = driver.find_element_by_id('usernameUser')
    usernameUser.send_keys(username)

    time.sleep(30)
    passwordUserText = driver.find_element_by_id('passwordUserText')
    time.sleep(4)
    passwordUserText.click()

    # 输入密码
    passwordUser = driver.find_element_by_id('passwordUser')
    time.sleep(2)
    passwordUser.send_keys(passwd)
    time.sleep(2)
    # 点击登陆
    btnSubmitUser = driver.find_element_by_id('btnSubmitUser')
    btnSubmitUser.click()
    time.sleep(3)

    ''' 获取驱动Cookie '''
    print("Cookie" * 30, driver.get_cookies())
    dict1_cookie = {}
    cookie_tmp = []
    for cookie in driver.get_cookies():
        data = "{}={}".format(cookie['name'], cookie['value'])
        dict1_cookie[cookie['name']] = cookie['value']
        cookie_tmp.append(data)
    _cookie = ';'.join(cookie_tmp)

    print(_cookie)

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Host": "my.58.com",
        "Cookie": _cookie
    }

    ''' 通过COOKIE抓取数据'''
    session = requests.session()
    return session, HEADERS


if __name__ == '__main__':
    session, HEADERS = login()
    response = session.get("https://my.58.com/index", headers=HEADERS)
    print(response.text, response.url)
