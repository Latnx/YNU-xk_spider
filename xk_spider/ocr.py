# -*- coding: utf-8 -*-
import base64
import hashlib
import time
import requests
from PIL import Image, UnidentifiedImageError

# OCR手写文字识别接口地址
URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"
# 应用APPID(必须为webapi类型应用,并开通手写文字识别服务,参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
APPID = "24ca6585"
# 接口密钥(webapi类型应用开通手写文字识别后，控制台--我的应用---手写文字识别---相应服务的apikey)
API_KEY = "2b316b1f536a96d1006f7da52aaa1034"

# 语种设置
language = "en"
# 是否返回文本位置信息
location = "false"


def getHeader():
    curTime = str(int(time.time()))
    param = "{\"language\":\"" + language + "\",\"location\":\"" + location + "\"}"
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    str1 = API_KEY + curTime + str(paramBase64, 'utf-8')
    m2.update(str1.encode('utf-8'))
    checkSum = m2.hexdigest()
    # 组装http请求头
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def getBody(filepath):
    with open(filepath, 'rb') as f:
        imgfile = f.read()
    data = {'image': str(base64.b64encode(imgfile), 'utf-8')}
    return data


def getCaptcha_value(image_url):
    # 图片上传接口地址
    try:
        response = requests.get(image_url)
        with open("temp.jpg", "wb") as fh:
            fh.write(response.content)
        img = Image.open(".\\temp.jpg")
        img.resize((140, 60), Image.ANTIALIAS).save('imagetemp.png', 'png')

    except UnidentifiedImageError:
        print("UnidentifiedImageError")
        getCaptcha_value(image_url)

    picFilePath = ".\\imagetemp.png"
    r = requests.post(URL, headers=getHeader(), data=getBody(picFilePath))
    try:
        result = r.json()['data']['block'][0]['line'][0]['word'][0]['content']
    except:
        return getCaptcha_value(image_url)
    print(result)
    if len(result) == 4 and result.isalnum():
        return result
    else:
        return getCaptcha_value(image_url)
