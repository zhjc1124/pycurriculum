from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json


# 按自行需要更改
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)


class UIMS(object):
    def __init__(self, user, pwd):
        self.cookies = self.login(user, pwd)
        self.session = requests.session()
        requests.utils.add_dict_to_cookiejar(self.session.cookies, self.cookies)

    def login(self, username, password):
        driver.get('http://uims.jlu.edu.cn')
        # 等待页面加载完毕
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "script")))
        print("success login")
        js = 'dojo.byId("txtUserName").focus();' \
             'var form = dojo.byId("loginForm");' \
             'form.j_username.value = "%s";' \
             'form.pwdPlain.value = "%s";' \
             'loginPage.clickSubmit();' % (username, password)
        driver.execute_script(js)
        cookies = {}
        for c in driver.get_cookies():
            if c['name'] != 'pwdStrength':
                cookies[c['name']] = c['value']
        return cookies

    def get_course(self):
        s = self.session
        r = s.post('http://uims.jlu.edu.cn/ntms/action/getCurrentUserInfo.do')
        user_info = json.loads(r.text)
        post_data = {
            "tag": "search@teachingTerm",
            "branch": "byId",
            "params": {
                "termId": user_info['defRes']['term_l']
            }
        }
        headers = {'Content-Type': 'application/json'}
        r = s.post('http://uims.jlu.edu.cn/ntms/service/res.do', json.dumps(post_data), headers=headers)
        start_date = json.loads(r.text)['value'][0]['startDate'].split('T')[0]

        post_data["params"]["studId"] = user_info['userId']
        post_data["branch"] = "default"
        post_data["tag"] = "teachClassStud@schedule"
        r = s.post('http://uims.jlu.edu.cn/ntms/service/res.do', json.dumps(post_data), headers=headers)
        return start_date, json.loads(r.text)['value']


if __name__ == '__main__':
    # user, pwd = input().split(',')
    user, pwd = 'user', 'pwd'
    print(UIMS(user, pwd).get_course())

