from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tools.config import Config
import time
import json
import os

#os.environ["webdriver.chrome.driver"] = os.getcwd()+os.sep+'drivers'+os.sep+'chromedriver.exe'
#print(os.environ["webdriver.chrome.driver"])
#sys.path.insert(0,os.getcwd()+os.sep+'drivers')

def getcookies(DEBUG=True):
    def check_cookies(cookiesBefore):
        cookies=[]
        cookiesAfter = driver.get_cookies()
        for cookie in cookiesAfter:
            name=cookie.get('name')
            for cookieb in cookiesBefore:
                if cookieb.get('name')==name:
                    break
            else:
                cookies.append(cookie)
        return cookies
    chrome_options = Options()
    if DEBUG==False:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://passport.baidu.com/v2/?login')
    print('获取cookies中...')
    driver.maximize_window()
    while True:
        config=Config('data/Login.txt')
        cookiesBefore = driver.get_cookies()
        driver.find_element_by_id('TANGRAM__PSP_3__footerULoginBtn').click()
        time.sleep(1.5)
        driver.find_element_by_id("TANGRAM__PSP_3__userName").clear()
        driver.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(config.get('username'))
        driver.implicitly_wait(5)
        time.sleep(1.5)
        driver.find_element_by_id("TANGRAM__PSP_3__password").clear()
        driver.find_element_by_id("TANGRAM__PSP_3__password").send_keys(config.get('pswd'))
        time.sleep(1.5)
        driver.find_element_by_id('TANGRAM__PSP_3__submit').click()
        driver.implicitly_wait(5)
        time.sleep(5)
        cookies=check_cookies(cookiesBefore)
        if cookies:
            print('已成功获取cookies')
            break
        else:
            flag=0
            print('自动获取失败，请在30s内自行输入密码...')
            for t in range(30):
                cookies=check_cookies(cookiesBefore)
                if cookies:
                    print('已成功获取cookies')
                    flag=1
                    break
                print('当前剩余{}秒'.format(30-t),end='\r')
                time.sleep(1)
            else:
                driver.refresh()
                input('请重新配置密码文件，确认无误后回车')
                time.sleep(3)
            if flag:
                break
    with open('data/cookies.json','wb') as c:
        c.write(json.dumps(cookies).encode())
    driver.quit()
    return cookies

def login(url,DEBUG=True):
    print('正在登录...')
    try:
        with open('data/cookies.json','rb') as c:
            cookies=json.loads(c.read().decode())
    except:
        cookies=getcookies(DEBUG)
    chrome_options = Options()
    if DEBUG==False:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.delete_all_cookies()
    time.sleep(3)
    driver.get(url)
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(3)
    #driver.refresh()
    driver.get(url) #防止由于登录审核而重定向到登录url
    print('登录成功')
    return driver

if __name__ == "__main__":
    print(getcookies(True))
    '''
    url='https://index.baidu.com/'
    driver=login(url)
    time.sleep(3)
    driver.quit()
'''
