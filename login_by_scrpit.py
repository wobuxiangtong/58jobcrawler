import time
import sys
import re
import json
import requests
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

username = '18800029214'
passwd = 'xxx150xxx40312'

''' 设置浏览器的User-Agent '''
desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = (
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
)
driver = webdriver.PhantomJS(
    executable_path='/Users/uni/phantomjs-2.1.1-macosx/bin/phantomjs', desired_capabilities=desired_capabilities)

driver.get('https://passport.58.com/login')
time.sleep(1)

''' 执行58js获取加密串 '''
rsaModulus = driver.find_element_by_id('rsaModulus').get_attribute('value')
rsaExponent = driver.find_element_by_id('rsaExponent').get_attribute('value')

''' 获取加密串密码 '''
timespan = str(int(round(time.time() * 1000)))
encrypt_passwd_1 = driver.execute_script(
    "return encodeURIComponent('%s')" % passwd)
print("encrypt_passwd_1", encrypt_passwd_1)
p1_user = "return encryptString('{}{}', '{}', '{}')"
encrypt_passwd = driver.execute_script(
    p1_user.format(timespan, encrypt_passwd_1, rsaExponent, rsaModulus))

Fingerprint2 = driver.execute_script('return new Fingerprint2().get()')

fingerprint = driver.find_element_by_id('fingerprint').get_attribute('value')

print("->" * 30, rsaModulus, rsaExponent, encrypt_passwd, fingerprint)
# getTokenId = driver.execute_script('return getTokenId()')
session = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Origin": "https://passport.58.com",
    'Content-Type': 'application/x-www-form-urlencoded',
    "Upgrade-Insecure-Requests": "1",
    'Referer': 'https://passport.58.com/login?path=http://my.58.com/?pts=' + str(int(round(time.time() * 1000)))
}

postData = {
    "source": "pc-login",
    "path": 'http://my.58.com/?pts=' + str(int(round(time.time() * 1000))),
    "password": encrypt_passwd,
    # "timesign": '',
    "isremember": "false",
    "callback": "successFun",
    "yzmstate": "",
    "fingerprint": "",
    "finger2": fingerprint,
    # "tokenId": getTokenId,s
    "username": username,
    "validcode": "",
    "vcodekey": "",
    "btnSubmit": "登录中..."
}

rep = session.post('https://passport.58.com/login/dologin',
                   data=postData, headers=headers)
match = re.search('\((\{.*?\})\)', rep.text)
if match:
    res_json = json.loads(match.group(1))
    print(res_json)
    if res_json['code'] == 0:
        print('登陆成功!')
    else:
        print(res_json['msg'])
