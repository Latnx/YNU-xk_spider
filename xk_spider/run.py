from concurrent.futures import ThreadPoolExecutor, as_completed

from Login import get_params

import GetCourse

# 程序运行后会打开浏览器进入选课登录页面，请登录进去直到能看到具体的课程，然后就可以把浏览器关了
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62 ',
    "Connection": "close"
}
url = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/*default/index.do'

stdCode = ' '  # 在''中填入你的学号
pswd = ' '  # 填你的密码,如果你有安全上的考虑也可以等浏览器打开了再填


headers['cookie'], headers['token'], batchCode = get_params(stdCode, pswd, free=True)
headers['Referer'] = 'http://xk.ynu.edu.cn/xsxkapp/sys/xsxkapp/*default/grablessons.do?token='+headers["token"]
gc = GetCourse.GetCourse(headers, stdCode, batchCode)
ec = ThreadPoolExecutor()

# 仿照例子填写，可填写多个
taskList = [ec.submit(gc.judge, '大学英语读写', '高帆', class_id='202120221YN300417000826', delete_name="大学英语读写", kind='主修')
            # ec.submit(gc.judge, '大学英语听说', '陈俊秋', class_id='202120221YN300417000726', delete_name="大学英语听说", kind='主修')
            ]
# def judge(self, course_name, teacher, delete_name='', delete_teacher='', class_id='', delete_id='', kind='素选'):
for future in as_completed(taskList):
    print(future.result())
