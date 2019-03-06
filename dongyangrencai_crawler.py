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
hl.update("123456".encode(encoding='utf-8'))
password = hl.hexdigest()



r_1 = ""
try:
    r_1 = requests.get("https://www.dyrc.gov.cn/webs/query.aspx?k=&r=30&h=000")
except Exception as e:
    print("请求超时1"*10)
    exit()


soup_1 = BeautifulSoup(r_1.text)
pages = math.ceil(int(soup_1.select('#pager font')[0].get_text())/10)

crawled_company_list = []

while page < pages:
    page+=1

    print("page->"*10,"%d/%d" % (page,pages),len(crawled_company_list))

    data = {"__VIEWSTATE":soup_1.select('#__VIEWSTATE')[0].get('value'),
        "__VIEWSTATEGENERATOR":soup_1.select('#__VIEWSTATEGENERATOR')[0].get('value'),
        "__EVENTTARGET":"pager",
        "__EVENTARGUMENT":"%d" % page,
        "__EVENTVALIDATION":soup_1.select('#__EVENTVALIDATION')[0].get('value'),
        "ddlRq" : "30",
        "ddlHy" : "000"
    }


    r_1 = ""
    most_retry_times = 3
    retry_times = 0
    while r_1 == "" and retry_times < most_retry_times:
        retry_times += 1
        try:
            r_1 = requests.post("https://www.dyrc.gov.cn/webs/query.aspx?k=&r=3&h=000",data = data,timeout = 3)
        except Exception as e:
            print("请求超时2"*10)
    if r_1 != "":
        soup_1 = BeautifulSoup(r_1.text)
        for company in soup_1.select(".job-list"):
            if company.select("a")[0].get('href').split('#')[0] not in crawled_company_list:
                # print("company"*300,company.select("a")[0].get('href').split('#')[0])
                crawled_company_list.append(company.select("a")[0].get('href').split('#')[0])
                
                r_2 = ""
                retry_times = 0
                while r_2 == "" and retry_times < most_retry_times:
                    retry_times += 1
                    try:
                        r_2 = requests.get("https://www.dyrc.gov.cn"  + company.select("a")[0].get('href').split('#')[0],timeout = 3)
                    except Exception as e:
                        print("请求超时3"*10)
                if r_2 != "":
                    r_2.encoding = 'utf-8'
                    soup_2 = BeautifulSoup(r_2.text)
                    company_name = soup_2.select(".company_cont_bg > h1")[0].get_text()
                    # print("company_name",company_name)
                    company_table = soup_2.select(".company_table td")[1::2]
                    # print(company_table)
                    trade_name = company_table[0].get_text()
                    # scale = company_table[1].get_text().split("-")[0]
                    in_manager = company_table[4].get_text()
                    in_manager_mobile = re.findall(r'((\(?0\d{2,3}[)-]?)?\d{7,11})',company_table[5].get_text())
                    if len(in_manager_mobile) == 0:
                        continue
                    else:
                        in_manager_mobile = in_manager_mobile[0][0]
                    address = company_table[6].get_text()
                    web_url = company_table[7].get_text()
                    # print("trade_name",trade_name,"scale",scale,"in_manager",in_manager,"in_manager_mobile",in_manager_mobile,"address",address,"web_url",web_url)
                    description = remove_emoji(soup_2.select('.company_base p')[0].get_text())
                    # print("description",description)
                    
                    cursor_1 = mysql_connector.cursor(buffered=True)
                    cursor_1.execute("select id from t_company where name = '%s'" % company_name)
                    if cursor_1.rowcount == 0:
                        cursor_1.execute("insert into t_company (`name`,`trade_name`,`address`,`web_url`,`description`,`company_source`,`province`,`city_name`,`district`) values ('%s','%s','%s','%s','%s',2,'浙江省','金华市','东阳市')" % (company_name,trade_name,address,web_url,description))
                        mysql_connector.commit()
                        company_id = cursor_1.lastrowid
                        cursor_1.execute("insert into t_hr (`name`,`show_mobile_num`,`company_id`,`hr_source`) values ('%s','%s',%d,2)" % (in_manager,in_manager_mobile,company_id))
                        mysql_connector.commit()
                        hr_id = cursor_1.lastrowid

                        company_job_titles = soup_2.select(".company_job_titlebg")
                        company_job_details = soup_2.select(".company_job_table")
                        company_job_contents = soup_2.select(".company_job_word")
                        company_job_index = -1
                        for job_title in company_job_titles:
                            company_job_index += 1
                            position_name = job_title.get_text()
                            job_detail = company_job_details[company_job_index].select("td")[1::2]
                            position_address = job_detail[0].get_text()
                            # min_salary = job_detail[1].get_text().split("-")[0]


                            salary = re.findall(r'\d+',job_detail[1].get_text())
                            if len(salary) != 0:
                                salary = int(salary[0])//500
                            else:
                                salary = -1

                            last_refresh_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            refresh_date = last_refresh_date
                            hire_num = re.findall(r'\d+',job_detail[4].get_text())
                            if len(hire_num) != 0:
                                hire_num = hire_num[0]
                            else:
                                hire_num = "1"

                            requirement = remove_emoji("专业要求: %s;\n学历要求: %s; \n工作经验: %s;\n其他要求: %s" % (job_detail[6].get_text(),job_detail[7].get_text(),job_detail[8].get_text(),job_detail[9].get_text()))
                            content = remove_emoji(company_job_contents[company_job_index].get_text())
                            cursor_1.execute("insert into t_position (`company_id`,`hr_id`,`name`,`address`,`last_refresh_date`,`hire_num`,`requirement`,`content`,`refresh_date`,`salary`,`position_source`,`province`,`city_name`,`district`,`hide`) values (%d,%d,'%s','%s','%s','%s','%s','%s','%s',%d,2,'浙江省','金华市','东阳市',1)" % (company_id,hr_id,position_name,position_address,last_refresh_date,hire_num,requirement,content,refresh_date,salary))
                            mysql_connector.commit()
                # print("name",job_title.get_text(),"address",address,"min_salary",min_salary,"salary",salary,"hire_num",hire_num,"requirement",requirement,"content",content)