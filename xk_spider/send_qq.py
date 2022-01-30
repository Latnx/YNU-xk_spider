# 发送消息
import json


def send_qq(msg):
    import requests
    token = ' '  # 在pushplus网站中可以找到
    with open("info.json", 'r') as f:
        token = json.loads(f.read())['user']['token']
    title = 'test'  # 改成你要的标题内容
    content = msg  # 改成你要的正文内容
    url = 'http://pushplus.hxtrip.com/send?token=' + token + '&title=' + title + '&content=' + content
    requests.get(url)


if __name__ == '__main__':
    send_qq('测试')
