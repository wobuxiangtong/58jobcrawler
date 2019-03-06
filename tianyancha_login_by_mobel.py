# -*- coding: utf-8 -*-
import time
import sys
import re
import requests
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from PIL import Image
from bs4 import BeautifulSoup


def tianyancha_login():

    username = '18811029214'
    passwd = 'xyf15038140312'

    driver = webdriver.Chrome(executable_path='/Users/uni/chromedriver')
    driver.get(
        'https://www.tianyancha.com/login')
    time.sleep(3)
    pwdLogin = driver.find_elements_by_xpath(
        "//input[@class='input contactphone']")
    pwdLogin[3].send_keys(username)
    time.sleep(4)
    dcoderSelect = driver.find_element_by_id(
        "smsCodeBtnPopup")
    dcoderSelect.click()
    print("手机动态码登陆")
    input_dcode = input("请输入验证码")

    passwordUser = driver.find_elements_by_xpath(
        "//input[@class='input contactscode']")
    passwordUser[1].send_keys(input_dcode)
    time.sleep(3)
    btnSubmit = driver.find_elements_by_xpath(
        "//div[@class='btn -hg btn-primary -block']")
    btnSubmit[3].click()
    # print("click 手机动态码登陆")
    time.sleep(2)

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


    ''' 通过COOKIE抓取数据'''
    session = requests.session()
    return session, dict1_cookie


if __name__ == '__main__':
    _, cookies = tianyancha_login()
    response = requests.get(
        "https://www.tianyancha.com/search?key=北京景天信息技术有限公司", cookies=cookies)
    print(response.text, "--------->", response.url)
    soup_2 = BeautifulSoup(response.text, features="html5lib")
    print(soup_2.select('.tt .hidden')[0].get_text())
    time.sleep(10)
    print(response.url)
