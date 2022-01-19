## 修改部分

- 增加自动退课功能
- 新增使用课程号辅助搜索，防止歪课

- 修改自动登录模块，实现自动识别验证码并登录
- 修复长时间登录，被强制下线问题

## 自定义部分
- run.py 中的账号和密码

- send_qq.py 中的token值，在https://pushplus.hxtrip.com 获取 

- run.py 中填写抢课内容 （*为选填）

  | 变量名         | 作用            |
  | -------------- | --------------- |
  | course_name    | 待抢课程名      |
  | teacher        | 待抢课程教师    |
  | delete_name    | *删除课程名     |
  | delete_teacher | *删除课程教师名 |
  | class_id       | *待抢课程id     |
  | delete_id      | *删除课程id     |
  | kind           | 课程种类        |

- chargeOCR.py 中 uname和 pwd，在http://www.kuaishibie.cn/ 获得（增加识别成功率，非必须）

- ocr.py 内置使用使用讯飞 api, 若使用额度用尽，可自定义 api（非必须）

## 使用方法

1. 安装好环境，将chrome驱动放在python目录下
2. 修改自定义部分
3. 点击run.bat开始运行，若能出现正确提示则运行成功
