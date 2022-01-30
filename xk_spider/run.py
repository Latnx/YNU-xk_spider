import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from Login import get_params

import GetCourse
import GUI

# 程序运行后会打开浏览器进入选课登录页面，请登录进去直到能看到具体的课程，然后就可以把浏览器关了
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62 ',
    "Connection": "close"
}
url = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do'

GUI.login_gui()

f = open("info.json", "r")
info = json.loads(f.read())

stdCode = info['user']['num']
pswd = info['user']['psw']

headers['cookie'], headers['token'], batchCode = get_params(stdCode, pswd, free=True)
headers['Referer'] = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/*default/grablessons.do?token=' + headers["token"]
gc = GetCourse.GetCourse(headers, stdCode, batchCode)
ec = ThreadPoolExecutor()

taskList = []
for course in info["course_list"]:
    taskList.append(ec.submit(gc.judge,
                              course['course_name'],
                              course['teacher'],
                              course['delete_name'],
                              course['delete_teacher'],
                              course['class_id'],
                              course['delete_id'],
                              course['素选']))
for future in as_completed(taskList):
    print(future.result())
