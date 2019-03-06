import requests
from bs4 import BeautifulSoup
from datetime import datetime
import math
import hashlib
import re


page = 0



    

# print(r_1.text)
print('\n','*'*200,'\n')




position_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'ijob_position',
    'user': 'root',
    'password': 'root',
    'charset': 'utf8',
}





# emoji_pattern = 
try:
    # Wide UCS-4 build
    emoji_pattern = re.compile(u'['
        u'\U0001F300-\U0001F64F'
        u'\U0001F680-\U0001F6FF'
        u'\u2600-\u2B55]+',
        re.UNICODE)
except re.error:
    # Narrow UCS-2 build
    emoji_pattern = re.compile(u'('
        u'\ud83c[\udf00-\udfff]|'
        u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
        u'[\u2600-\u2B55])+',
        re.UNICODE)

def remove_emoji(text):
    return emoji_pattern.sub(r'', text)


from mysql_connection import MySqlClient

mysql_client = MySqlClient()
mysql_connector = mysql_client.get_connection(position_config)


hl = hashlib.md5()
hl.update("hengxin666".encode(encoding='utf-8'))
password = hl.hexdigest()

cookies_str = "UM_distinctid=169131b2e3b8b3-0d5ad99052fa1a-1333063-1aeaa0-169131b2e3c303; bdshare_firstime=1550804522384; ak888=userid=122347&username=xxx__1&truename=%e9%ad%8f%e4%bb%80%e4%b9%88&userstatus=1&lastlogintime=2019/3/4 16:40:24&lastip=122.144.218.133&usertype=2&userpwd=%2bOPIBrYUv879Ix3itm6ozulZrJoN20DLBTsvsa1u%2fvULgrsAExI4pw%3d%3d&usergroup=0&resumestatus=1; CNZZDATA4649955=cnzz_eid%3D1542819897-1550799698-null%26ntime%3D1551684829"

cookies = {cookie.split("=")[0]:"=".join(cookie.split("=")[1:]) for cookie in cookies_str.split(";")}


print(cookies)

r_1 = ""
try:
    r_1 = requests.get("http://www.ankang888.com/jobs.aspx?Pager1=1")
except Exception as e:
    print("请求超时1"*10)
    exit()


soup_1 = BeautifulSoup(r_1.text)
pages = len(list(soup_1.select('option')))

crawled_company_list = []

while page < pages:
    page+=1

    print("page->"*10,"%d/%d" % (page,pages),len(crawled_company_list))

    # data = {"__VIEWSTATE":soup_1.select('#__VIEWSTATE')[0].get('value'),
    #     "__VIEWSTATEGENERATOR":soup_1.select('#__VIEWSTATEGENERATOR')[0].get('value'),
    #     "__EVENTTARGET":"pager",
    #     "__EVENTARGUMENT":"%d" % page,
    #     "__EVENTVALIDATION":soup_1.select('#__EVENTVALIDATION')[0].get('value'),
    #     "ddlRq" : "30",
    #     "ddlHy" : "000"
    # }


    r_1 = ""
    most_retry_times = 3
    retry_times = 0
    while r_1 == "" and retry_times < most_retry_times:
        retry_times += 1
        try:
            r_1 = requests.get("http://www.ankang888.com/jobs.aspx?Pager1=%d" % page)
        except Exception as e:
            print("请求超时2"*10)
    if r_1 != "":
        soup_1 = BeautifulSoup(r_1.text)
        for company in soup_1.select(".gt2 a"):
            if company.get('href') not in crawled_company_list:
                print(company.get('href'))
                # print("company"*300,company.select("a")[0].get('href').split('#')[0])
                crawled_company_list.append(company.get('href'))
                
                r_2 = ""
                retry_times = 0
                while r_2 == "" and retry_times < most_retry_times:
                    retry_times += 1
                    try:
                        r_2 = requests.get(company.get('href'),timeout = 3,cookies = cookies)
                    except Exception as e:
                        print("请求超时3"*10)
                if r_2 != "" and "招聘企业已关闭" not in r_2.text and "堆栈跟踪" not in r_2.text:
                    company_name = company.get_text().strip()
                    r_2.encoding = 'utf-8'
                    # print(r_2.text,r_2.url)

                    soup_2 = BeautifulSoup(r_2.text)
                    print("company_name",company_name)
                    logo = "http://www.ankang888.com" + soup_2.select(".gsjs img")[0].get("src")
                    # print(logo)
                    description = remove_emoji(soup_2.select('.gsjs')[0].get_text())
                    trade_name = soup_2.select('.gz6_1')[0].get_text().split("：")[1]

                    in_manager = soup_2.select('.gz5 li')[1].get_text().split('：')[1]                    
                    in_manager_mobile = re.findall(r'((\(?0\d{2,3}[)-]?)?\d{7,11})',soup_2.select('.gz5 li')[2].get_text().split('：')[1])
                    if len(in_manager_mobile) == 0:
                        continue
                    else:
                        in_manager_mobile = in_manager_mobile[0][0]

                    email = soup_2.select('.gz5 li')[4].get_text().split('：')[1]
                    address = soup_2.select('.gz5 li')[5].get_text().split('：')[1]
                    web_url = soup_2.select('.gz5 li')[6].get_text().split('：')[1]
                    print(description,trade_name,in_manager,in_manager_mobile,email,address,web_url)

                    cursor_1 = mysql_connector.cursor(buffered=True)
                    cursor_1.execute("select id from t_company where name = '%s'" % company_name)
                    # print("select id from t_company where name = '%s'" % company_name)
                    if cursor_1.rowcount == 0:
                        cursor_1.execute("insert into t_company (`name`,`trade_name`,`address`,`web_url`,`description`,`logo`,`company_source`,`province`,`city_name`,`district`) values ('%s','%s','%s','%s','%s','%s',3,'浙江省','金华市','东阳市')" % (company_name,trade_name,address,web_url,description,logo))
                        mysql_connector.commit()
                        company_id = cursor_1.lastrowid
                        cursor_1.execute("insert into t_hr (`name`,`show_mobile_num`,`company_id`,`email`,`hr_source`) values ('%s','%s',%d,'%s',3)" % (in_manager,in_manager_mobile,company_id,email))
                        mysql_connector.commit()
                        hr_id = cursor_1.lastrowid

                        jobs = soup_2.select(".gz7 li a")
                        # print(jobs,"jobs"*30)

                        for job in jobs:

                            r_3 = ""
                            retry_times = 0
                            while r_3 == "" and retry_times < most_retry_times:
                                retry_times += 1
                                try:
                                    r_3 = requests.get(job.get('href'),timeout = 3)
                                except Exception as e:
                                    print("请求超时3"*10)

                            soup_3 = BeautifulSoup(r_3.text)
                            job_detail = soup_3.select(".gz2 li")
                            
                            position_category = job_detail[0].get_text().replace("职位类型","")
                            position_sex = job_detail[1].get_text().replace("性别要求","")
                            position_exp = job_detail[2].get_text().replace("工作经验","")
                            position_age = job_detail[3].get_text().replace("年龄要求","")

                            position_education = job_detail[4].get_text().replace("学历要求","")
                            salary = re.findall(r'\d+',job_detail[5].get_text())
                            if len(salary) != 0:
                                salary = int(salary[0])//500
                            else:
                                salary = -1
                            hire_num = re.findall(r'\d+',job_detail[6].get_text())
                            position_address = job_detail[7].get_text().replace("工作地区","")
                            position_name = job.get_text()
                            content = remove_emoji(soup_3.select(".z2")[0].get_text())
                            
                            last_refresh_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                            if len(hire_num) != 0:
                                hire_num = hire_num[0]
                            else:
                                hire_num = "1"
                            requirement = ""
                            # print(position_name,position_category,position_sex,position_exp,position_age,position_education,salary,hire_num,position_address,position_name,content)
                            # print('-'*100)
                            cursor_1.execute("insert into t_position (`company_id`,`hr_id`,`name`,`address`,`last_refresh_date`,`hire_num`,`requirement`,`content`,`salary`,`category_name`,`refresh_date`,`position_source`,`province`,`city_name`,`district`,`hide`) values (%d,%d,'%s','%s','%s','%s','%s','%s',%d,'%s','%s',3,'浙江省','金华市','东阳市',1)" % (company_id,hr_id,position_name,position_address,last_refresh_date,hire_num,requirement,content,salary,position_category,last_refresh_date))
                            mysql_connector.commit()
                # print("name",job_title.get_text(),"address",address,"min_salary",min_salary,"salary",salary,"hire_num",hire_num,"requirement",requirement,"content",content)