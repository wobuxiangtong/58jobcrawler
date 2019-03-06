import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
from uni_decrypt import AESCipher
from tongcheng_login_by_mobel import tongcheng_login
from tianyancha_login_by_mobel import tianyancha_login


import json
import hashlib

# 58同城 电话号码解码key值
key = '5749812cr3419i8s'
aes = AESCipher(key)

#  手机验证码登陆
session_tongcheng, HEADERS_TONGCHENG, dict_cookie_tongcheng = tongcheng_login()
_, cookies_tianyancha = tianyancha_login()

mysql_client = MySqlClient()
position_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'ijob_position',
    'user': 'root',
    'password': 'root',
    'charset': 'utf8',
}
from mysql_connection import MySqlClient
mysql_connector = mysql_client.get_connection(position_config)

hl = hashlib.md5()
hl.update("123456".encode(encoding='utf-8'))
password = hl.hexdigest()

# 58同城分类接口
r_1 = requests.get('https://api.58.com/comm/cate/?api_type=json&api_pid=9224')

for category_1 in r_1.json()["comms_getcatelist"]:
    print("category_1", category_1)
    category_1_name = category_1["cateName"]
    r_2 = requests.get(
        'https://api.58.com/comm/cate/?api_type=json&api_pid=%d' % category_1["dispCategoryID"])
    for category_2 in r_2.json()["comms_getcatelist"]:
        print("category_2", category_2)
        category_2_name = category_2["cateName"]
        page_count = 0
        while True:
            page_count += 1
            print("https://zprecommend.58.com/api/abtest?ptype=pc_detail_new&dispcateid=%d&displocalid=536&page=%d&postdate=%s_%s" %
                  (category_2["dispCategoryID"], page_count, datetime.now().strftime('%Y%m%d'), (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')))
            r_3 = requests.get("https://zprecommend.58.com/api/abtest?ptype=pc_detail_new&dispcateid=%d&displocalid=536&page=%d&postdate=%s_%s" % (
                category_2["dispCategoryID"], page_count, datetime.now().strftime('%Y%m%d'), (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')))

            if r_3.json()["pc_detail_new"] == "":
                break
            for position in r_3.json()["dataList"]:
                # 职位基础信息
                print("https://dongyang.58.com/%s/%dx.shtml" %
                      (position["catelistname"], position["id"]))
                r_4 = requests.get("https://dongyang.58.com/%s/%dx.shtml" %
                                   (position["catelistname"], position["id"]))

                while "verifycode" in r_4.url:
                    # print("验证码" * 100)
                    from selenium import webdriver
                    driver = webdriver.Chrome(
                        executable_path='/Users/uni/chromedriver')
                    driver.get(r_4.url)
                    for name, value in dict_cookie_tongcheng.items():

                        driver.add_cookie({"name": name, "value": value})

                    input("58验证码" * 100)
                    r_4 = requests.get("https://dongyang.58.com/%s/%dx.shtml" %
                                       (position["catelistname"], position["id"]))

                print(position)

                # 职位要求以及岗位职责
                soup = BeautifulSoup(r_4.text, features="html5lib")
                position_content = soup.select('.des')[0].get_text()
                print(soup.select('.des')[0].get_text())

                # hr 电话号码

                HEADERS_1 = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    "Host": "zpservice.58.com",
                    "Referer": "https://qy.58.com/46414996073492/?entinfo=%d_0" % position["id"],
                    "Cookie": 'id58=c5/njVw+nqxJD6CFAz/fAg==; 58tj_uuid=71949cfb-a332-4d53-99e1-5ba15686a0f5; als=0; xxzl_deviceid=xNd%2Bz%2FGhL8auyLYnhOkvhtWzm%2FFa7Y%2Fw2tYGN7nLkNjw%2FntQvxZ8gAyRhbCQhjBv; wmda_uuid=cb77c0441742bbe950d8fdab80b142a4; wmda_new_uuid=1; wmda_visited_projects=%3B1731916484865; sessionid=0f2fc1cf-f4f4-4a8a-aa9b-3ed271268b03; gr_user_id=08587eba-3400-4e32-81ba-fb0c6f6eb77f; f=n; 58home=changningx; xxzl_smartid=38a4f9a6c5c1c34f880d8820ac1f1e3; __utmc=253535702; myfeet_tooltip=end; bangtoptipclose=1; new_uv=5; utm_source=; spm=; init_refer=https%253A%252F%252Fqy.58.com%252F46414996073492%252F%253Fentinfo%253D34967427868477_0%2526PGTID%253D0d40254a-03a7-d88d-9364-8885f6b97967%2526ClickID%253D8; new_session=0; wmda_session_id_1731916484865=1551061607712-ee3fa1b6-2566-9fe8; www58com="UserID=36929129940752&UserName=%E6%88%91%E4%B8%8D%E6%83%B3%E9%80%9A"; 58cooper="userid=36929129940752&username=%E6%88%91%E4%B8%8D%E6%83%B3%E9%80%9A"; 58uname=%E6%88%91%E4%B8%8D%E6%83%B3%E9%80%9A; gr_session_id_b4113ecf7096b7d6=4145efa3-d1ac-4ebb-a1c2-1d9013bb35c2; gr_session_id_b4113ecf7096b7d6_4145efa3-d1ac-4ebb-a1c2-1d9013bb35c2=true; __utma=253535702.1221022936.1550827475.1551061607.1551063709.5; __utmz=253535702.1551063709.5.5.utmcsr=dongyang.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/yewu/34967427868477x.shtml; __utmt_pageTracker=1; PPU="UID=36929129940752&UN=%E6%88%91%E4%B8%8D%E6%83%B3%E9%80%9A&TT=1c996342d625d6ac59ab885c02f82995&PBODY=Umh4vbYw9mrM8eRe7K0VjZQPPCfQg3RtKXpmP67pwTCbI0GWh6getCkNkDNOl_ajlQfro36cEymwgBye6TQTqJUvtGj5PDtDKx1tp58upMLFuyZL37umtMwjZ3NNI61r3L9g7gwTr4FNDclDN6PuOVz_EK8bDbKKNJuzA9Q8jao&VER=1"; ppStore_fingerprint=935C0BE50304DA7F01A1EF88D6F5133B833847150E17555D%EF%BC%BF1551064690017; JSESSIONID=FFE68C5E23AF91121ABCFDAC8918C0F3; __utmb=253535702.6.10.1551063709'
                }

                HEADERS_TONGCHENG["Host"] = "zpservice.58.com"
                HEADERS_TONGCHENG["Referer"] = "https://qy.58.com/46414996073492/?entinfo=%d_0" % position["id"]

                r_5 = session_tongcheng.get(
                    "https://zpservice.58.com/numberProtection/biz/enterprise/pcBind/?uid=%d" % position["userid"], headers=HEADERS_TONGCHENG)
                mobile_num = ''
                if r_5.json().get("virtualNum") not in [None, ""]:
                    print("phone number" * 100,
                          aes.decrypt(r_5.json().get("virtualNum")))
                    mobile_num = aes.decrypt(r_5.json().get("virtualNum"))
                else:
                    print(r_5.json().get("msg") * 100)

                r_6 = requests.get(
                    "https://www.tianyancha.com/search?key=%s" % position["enterprisename"], cookies=cookies_tianyancha)
                while "antirobot" in r_6.url:
                    from selenium import webdriver
                    driver = webdriver.Chrome(
                        executable_path='/Users/uni/chromedriver')
                    driver.get(r_6.url)
                    for name, value in cookies_tianyancha.items():
                        driver.add_cookie({"name": name, "value": value})

                    input("天眼查验证码" * 100)
                    r_6 = requests.get(
                        "https://www.tianyancha.com/search?key=%s" % position["enterprisename"], cookies=cookies_tianyancha)
                    print("tianyanche1" * 100, r_6.url)
                    while "login" in r_6.url:
                        _, cookies_tianyancha = tianyancha_login()
                        r_6 = requests.get(
                            "https://www.tianyancha.com/search?key=%s" % position["enterprisename"], cookies=cookies_tianyancha)
                        print("tianyanche2" * 100, r_6.url)

                soup_2 = BeautifulSoup(r_6.text, features="html5lib")

                if len(soup_2.select('.tt')) != 0:

                    company_info = json.loads(soup_2.select(
                        '.tt')[0].get_text().replace('\t', ''))
                    cursor_1 = mysql_connector.cursor(buffered=True)
                    cursor_1.execute("insert into `t_company` (`name`,`in_manager`,`establish_date`,`description`,`address`,`logo`,`city_name`,`district`,`web_url`,`abbreviation`,`latitude`,`longitude`,`trade_name`,`type`) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%.4f,%.4f,'%s',-1000)" % (
                        company_info['name'], company_info['legalPersonName'], company_info["estiblishTime"][:19], company_info['businessScope'], company_info['regLocation'], company_info['logo'], company_info['city'], company_info['district'], company_info['websites'], company_info['abbr'], company_info['latitude'], company_info['longitude'], company_info['categoryStr']))
                    mysql_connector.commit()
                    print("sql" * 100, "insert into `t_company` (`name`,`in_manager`,`establish_date`,`description`,`address`,`logo`,`city_name`,`district`,`web_url`,`abbreviation`,`latitude`,`longitude`,`trade_name`) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%.4f,%.4f,'%s')" %
                          (company_info['name'], company_info['legalPersonName'], company_info["estiblishTime"][:19], company_info['businessScope'], company_info['regLocation'], company_info['logo'], company_info['city'], company_info['district'], company_info['websites'], company_info['abbr'], company_info['latitude'], company_info['longitude'], company_info['categoryStr']))
                    cursor_1.execute(
                        "select `id`,`type` from `t_company` where `name` = '%s'" % company_info['name'])

                    print('count' * 100, cursor_1.rowcount)
                    if cursor_1.rowcount != 0:
                        "新进入企业"
                        print("sql" * 100, "insert into `t_company` (`name`,`in_manager`,`establish_date`,`description`,`address`,`logo`,`city_name`,`district`,`web_url`,`abbreviation`,`latitude`,`longitude`,`trade_name`,`type`) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%.4f,%.4f,'%s',-1000)" % (
                            company_info['name'], company_info['legalPersonName'], company_info["estiblishTime"][:19], company_info['businessScope'], company_info['regLocation'], company_info['logo'], company_info['city'], company_info['district'], company_info['websites'], company_info['abbr'], company_info['latitude'], company_info['longitude'], company_info['categoryStr']))
                        cursor_1.execute("insert into `t_company` (`name`,`in_manager`,`establish_date`,`description`,`address`,`logo`,`city_name`,`district`,`web_url`,`abbreviation`,`latitude`,`longitude`,`trade_name`,`type`) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%.4f,%.4f,'%s',-1000)" % (
                            company_info['name'], company_info['legalPersonName'], company_info["estiblishTime"][:19], company_info['businessScope'], company_info['regLocation'], company_info['logo'], company_info['city'], company_info['district'], company_info['websites'], company_info['abbr'], company_info['latitude'], company_info['longitude'], company_info['categoryStr']))
                        mysql_connector.commit()
                        company_id = cursor_1.lastrowid
                        print('company info' * 100, company_info)
                        if mobile_num == "":
                            mobile_num = company_info['phoneNum']
                        print("sql" * 100, "insert into t_hr (`email`,`mobile_num`,`name`,`username`,`company_id`,`password`) values ('%s','%s','%s','%s',%d,'%s')" % (
                            company_info['emails'], mobile_num, company_info['legalPersonName'], company_info['name'], company_id, password))
                        cursor_1.execute("insert into t_hr (`email`,`mobile_num`,`name`,`username`,`company_id`,`password`) values ('%s','%s','%s','%s',%d,'%s')" % (
                            company_info['emails'], mobile_num, company_info['legalPersonName'], company_info['name'], company_id, password))
                        mysql_connector.commit()
                        hr_id = cursor_1.lastrowid
                        print("sql" * 100, "insert into `t_position` (`min_salary`,`salary`,`welfare_tags`,`city_name`,`district`,`category_name`,`name`,`create_date`,`content`,`company_id`,`hr_id`) values (%s,%s,'%s','%s','%s','%s','%s','%s','%s',%d,%d)" % (position['salary'].split(
                            '-')[0], position['salary'].split('-')[1], position['welfare'], company_info['city'], company_info['district'], position['jobname'], position['title'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(position['posttimestemp'] / 1000)), soup.select('.des')[0].get_text(), company_id, hr_id))
                        cursor_1.execute("insert into `t_position` (`min_salary`,`salary`,`welfare_tags`,`city_name`,`district`,`category_name`,`name`,`create_date`,`content`,`company_id`,`hr_id`) values (%s,%s,'%s','%s','%s','%s','%s','%s','%s',%d,%d)" % (position['salary'].split(
                            '-')[0], position['salary'].split('-')[1], position['welfare'], company_info['city'], company_info['district'], position['jobname'], position['title'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(position['posttimestemp'] / 1000)), soup.select('.des')[0].get_text(), company_id, hr_id))
                        mysql_connector.commit()

                time.sleep(60)
                # break
            break
        break
    break
