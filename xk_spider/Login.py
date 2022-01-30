import json
import time

from lxml import etree
from selenium import webdriver
from chargeOCR import base64_api
from ocr import getCaptcha_value
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from send_qq import send_qq
from GUI import captcha_handle


def get_params(username, password, free):
    # 操作浏览器

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/86.0.4240.198 Safari/537.36')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    url = 'http://xk.ynu.edu.cn'
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_id('loginName').send_keys(username)
    time.sleep(1)
    driver.find_element_by_id('loginPwd').send_keys(password)
    time.sleep(1)

    # 获取验证码相关信息 得到验证码的url
    html_str = driver.page_source
    html_ele = etree.HTML(html_str)
    image_url = html_ele.xpath('//img[@id="vcodeImg"]/@src')[0]


    i = 0
    n = 0
    while True:
        response = requests.get(image_url)
        with open(".\\temp.jpg", "wb") as fh:
            fh.write(response.content)
        # 三次免费识别失败自动转为付费模式
        if free and n > 3:
            free = False
            n = 0
            print("付费模式启动")
            send_qq("付费模式启动")

        driver.find_element_by_id('verifyCode').clear()
        # 免费讯飞api调用
        if free:
            captcha_value = getCaptcha_value(image_url)
        # 两种自动识别失败后，使用手动模式添加
        elif not free and n > 1:
            print("自动验证失败")
            captcha_value = captcha_handle()
        # 收费调用 识别率高 0.002元/次
        else:
            captcha_value = base64_api()

        driver.find_element_by_id('verifyCode').send_keys(captcha_value)
        time.sleep(1)
        driver.find_element_by_id('studentLoginBtn').click()
        time.sleep(1)
        i += 1
        n += 1
        try:
            WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div[2]/button[2]')))
            print('判定成功')
            send_qq('判定成功')
            break
        except:
            pass
        send_qq(f'第{i}次尝试失败')
        print(captcha_value)
    # 进入选课界面
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/button[2]').click()
    time.sleep(1)
    driver.find_element_by_id('courseBtn').click()

    # 解析登陆数据
    cookie_lis = driver.get_cookies()
    cookies = ''
    for item in cookie_lis:
        cookies += item['name'] + '=' + item['value'] + '; '
    token = driver.execute_script('return sessionStorage.getItem("token");')
    batch_str = driver.execute_script('return sessionStorage.getItem("currentBatch");')
    batch = json.loads(batch_str)
    time.sleep(2)
    driver.close()
    return cookies, token, batch['code']

