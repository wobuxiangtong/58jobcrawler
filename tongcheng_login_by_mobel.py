# -*- coding: utf-8 -*-
import time
import sys
import re
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from PIL import Image


def tongcheng_login():

    username = '18811029214'
    driver = webdriver.Chrome(executable_path='/Users/uni/chromedriver')
    driver.get(
        'https://passport.58.com/login')
    time.sleep(1)
    pwdLogin = driver.find_element_by_id('pwdLogin')
    pwdLogin.click()
    time.sleep(3)
    dcoderSelect = driver.find_elements_by_xpath(
        "//ul[@id='loginBoxTitle']/li")
    dcoderSelect[1].click()
    print("click 手机动态码登陆")
    time.sleep(3)

    # 输入用户名
    usernameUser = driver.find_element_by_id('loginMobile')
    usernameUser.send_keys(username)

    time.sleep(3)
    passwordUserText = driver.find_element_by_id('loginMobilecodeSendBtn')
    time.sleep(4)
    passwordUserText.click()

    # 输入密码
    passwordUser = driver.find_element_by_id('loginMobilecode')
    time.sleep(2)
    input_dcode = input("请输入验证码")
    passwordUser.send_keys(input_dcode)
    time.sleep(2)
    # 点击登陆
    btnSubmitUser = driver.find_element_by_id('loginMobileButton')
    btnSubmitUser.click()
    time.sleep(3)

    ''' 获取驱动Cookie '''
    # print("Cookie" * 30, driver.get_cookies())
    dict1_cookie = {}
    cookie_tmp = []
    for cookie in driver.get_cookies():
        data = "{}={}".format(cookie['name'], cookie['value'])
        dict1_cookie[cookie['name']] = cookie['value']
        cookie_tmp.append(data)
    _cookie = ';'.join(cookie_tmp)

    print("dict cookies", dict1_cookie, "string cookies", _cookie)

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        # "Host": "my.58.com",
        "Cookie": _cookie
    }

    ''' 通过COOKIE抓取数据'''
    session = requests.session()
    return session, HEADERS, dict1_cookie


if __name__ == '__main__':
    session, HEADERS, dict1_cookie = tongcheng_login()
    response = session.get("https://my.58.com/index", headers=HEADERS)
    print(response.text, response.url)
