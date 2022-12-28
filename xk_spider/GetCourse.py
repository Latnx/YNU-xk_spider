import json
import random
import re
import time

import requests
from requests.exceptions import HTTPError

from send_qq import send_qq


class GetCourse:
    def __init__(self, headers: dict, stdcode, batchcode):
        self.headers = headers
        self.stdcode = stdcode
        self.batchcode = batchcode

    def judge(self, course_name, teacher, delete_name='', delete_teacher='', class_id='', delete_id='', kind='素选'):
        # 人数未满才返回classId
        if kind == '素选':
            kind = 'publicCourse.do'
            class_type = "XGXK"
        elif kind == '主修':
            kind = 'programCourse.do'
            class_type = "FANKC"
        else:
            class_type = "QXKC"

        url = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/elective/' + kind
        query = self.__judge_datastruct(course_name, class_type)
        while True:
            try:
                r = requests.post(url, data=query, headers=self.headers, timeout=30)
                r.raise_for_status()
                flag = 0
                while not r:
                    if flag > 2:
                        print(f'{course_name} 查询失败，请检查失败原因', '线程结束')
                        send_qq(f'{course_name} 查询失败，请检查失败原因' + '线程结束')
                        return False
                    print(f'[warning]: jugde()函数正尝试再次爬取')
                    send_qq(f'[warning]: jugde()函数正尝试再次爬取')
                    time.sleep(3)
                    r = requests.post(url, data=query, headers=self.headers)
                    flag += 1
                # 如果set-cookie 则将cookie中_WEU替换
                try:
                    set_cookie = r.headers['set-cookie']
                except KeyError:
                    set_cookie = ''
                if set_cookie:
                    print(f'[set-cookie]: {set_cookie}')
                    send_qq(f'[set-cookie]: {set_cookie}')
                    update = re.search(r'_WEU=.+?; ', set_cookie).group(0)
                    self.headers['cookie'] = re.sub(r'_WEU=.+?; ', update, self.headers['cookie'])
                    print(f'[current cookie]: {self.headers["cookie"]}')
                    send_qq(f'[current cookie]: {self.headers["cookie"]}')
                res = r.json()
                datalist = []
                if kind == 'publicCourse.do':
                    datalist = res['dataList']
                elif kind == 'programCourse.do':
                    datalist = res['dataList'][0]['tcList']
                elif kind == 'queryCourse.do':
                    datalist = res['dataList']

                if res['msg'] == '未查询到登录信息':
                    print('登录失效，请重新登录')
                    send_qq('登录失效，请重新登录')
                    return False
                MatchNum = 0
                for course in datalist:
                    if class_id not in course['teachingClassID']:
                        continue
                    if teacher not in course['teacherName']:
                        continue
                    MatchNum += 1
                    remain = int(course['classCapacity']) - int(course['numberOfFirstVolunteer'])
                    if remain > 0:
                        string = f'{course_name} {teacher}：已选{course["numberOfSelected"]}人，{remain}人空缺'
                        print(string)
                        send_qq(string)
                        if delete_name != '':
                            self.get_delete(delete_name, delete_teacher)
                        res = self.post_add(course_name, teacher, class_type, course['teachingClassID'])
                        return res

                if MatchNum == 0:
                    print(f"未找到{teacher}相匹配课程，请检查。")
                    raise TypeError

                print(f'{course_name} {teacher}：人数已满 {time.ctime()}')
                time.sleep(15 + random.randint(-3, 3))

            except HTTPError or SyntaxError:
                print('登录失效，请重新登录')
                send_qq('登录失效，请重新登录')
                return False
            except requests.exceptions.Timeout or requests.exceptions.ConnectionError:
                print("请求超时")
                self.random_ua()
                time.sleep(120)
            except TypeError:
                print('未找到相应课程，请检查')
                send_qq('未找到相应课程，请检查')
                time.sleep(15)
            # 不知名错误，反复重试
            except Exception as e:
                print(e)
                send_qq(str(e))
                time.sleep(30)

    def random_ua(self):
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
            'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; MI NOTE LTE Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/8.8.7',
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1',
            'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7',
            'Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Xoom Build/IML77) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Safari/535.7',
            'Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e YisouSpider/5.0 Safari/602.1',
            'Mozilla/5.0 (Linux; Android 4.0; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/59.0.3071.92',
            'Mozilla/5.0 (Linux; Android 6.0.1; SOV33 Build/35.0.D.0.326) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.91 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 6.0; HUAWEI MLA-AL10 Build/HUAWEIMLA-AL10) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 7.1.1; vivo X20A Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 VivoBrowser/5.6.1.1',
            'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; SM-J7108 Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.7.977 Mobile Safari/537.36',
            'Mozilla/6.0 (Linux; Android 8.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Mobile Safari/537.36'
        ]
        self.headers['User-Agent'] = random.choice(user_agent_list)

    def post_add(self, classname, teacher, class_type, class_id):
        query = self.__add_datastruct(class_id, class_type)

        url = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/elective/volunteer.do'
        r = requests.post(url, headers=self.headers, data=query)
        flag = 0
        while not r:
            if flag > 2:
                print(f'{classname} 有余课，但post未成功', '线程结束')
                send_qq(f'{classname} 有余课，但post未成功' + '线程结束')
                break
            print(f'[warning]: post_add()函数正尝试再次请求')
            send_qq(f'[warning]: post_add()函数正尝试再次请求')
            time.sleep(3)
            r = requests.post(url, headers=self.headers, data=query)
            flag += 1
        message = r.json()['msg']
        title = '抢课结果'
        string = '[' + teacher + ']' + classname + ': ' + message
        print(title, string)
        send_qq(title + string)
        return string

    def get_delete(self, classname, teacher):

        flag = 0
        r = None
        while not r:
            if flag > 2:
                print(f'{classname} 退课失败', '线程结束')
                send_qq(f'{classname} 退课失败' + '线程结束')
                break
            elif flag > 0:
                print(f'[warning]: post_delete()函数正尝试再次请求')
                send_qq(f'[warning]: post_delete()函数正尝试再次请求')
                time.sleep(3)

            url = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/elective/deleteVolunteer.do'
            query = self.__delete_datastruct(classname, teacher)
            r = requests.get(url, headers=self.headers, params=query)
            flag += 1
        message = r.json()['msg']
        title = '退课结果'
        string = '[' + teacher + ']' + classname + ': ' + message
        print(title, string)
        send_qq(title + string)
        return string

    def get_class_id(self, classname, teacher):
        payload = {
            'timestamp': str(int(round(time.time() * 1000)) + 31589 - 1602),
            'studentCode': self.stdcode,
            'electiveBatchCode': self.batchcode
        }
        url = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/elective/courseResult.do'
        r = requests.get(url, params=payload, headers=self.headers)
        print(r.json()['msg'])
        datalist = r.json()['dataList']
        for course in datalist:
            if (classname in course['courseName']) and (teacher in course['teacherName']):
                return course['teachingClassID']

    def __judge_datastruct(self, course, class_type) -> dict:
        data = {
            "data": {
                "studentCode": self.stdcode,
                "campus": "05",
                "electiveBatchCode": self.batchcode,
                "isMajor": "1",
                "teachingClassType": class_type,
                "checkConflict": "2",
                "checkCapacity": "2",
                "queryContent": course
            },
            "pageSize": "10",
            "pageNumber": "0",
            "order": ""
        }
        query = {
            'querySetting': str(data)
        }
        return query

    def __add_datastruct(self, class_id, class_type) -> dict:
        post_course = {
            "data": {
                "operationType": "1",
                "studentCode": self.stdcode,
                "electiveBatchCode": self.batchcode,
                "teachingClassId": class_id,
                "isMajor": "1",
                "campus": "05",
                "teachingClassType": class_type
            }
        }
        query = {
            'addParam': str(post_course)
        }
        return query

    def __delete_datastruct(self, classname, teacher) -> dict:

        class_id = self.get_class_id(classname, teacher)
        data = {
            "data": {
                "operationType": "2",
                "studentCode": self.stdcode,
                "electiveBatchCode": self.batchcode,
                "teachingClassId": class_id,
                "isMajor": "1"
            }
        }
        payload = {
            'timestamp': str(int(round(time.time() * 1000)) - 30000),
            'deleteParam': json.dumps(data)
        }
        return payload
