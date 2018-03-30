import requests
from bs4 import BeautifulSoup
import re
import time
from PIL import Image

# 构造 Request headers
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5'
headers = {
    "Host":"www.zhihu.com",
    "Referer":"https://www.zhihu.com/",
    "User-Agent":agent
}

session = requests.session()

# _xsrf 变化的参数，防止伪登录
def get_xsrf():
    index_url = "https://www.zhihu.com"
    index_page = session.get(url=index_url,headers=headers)
    index_soup = BeautifulSoup(index_page.text,"html.parser")
    xsrf_input = index_soup.find("input",{"name":"_xsrf"})
    xsrf_token = xsrf_input["value"]
    # print("获取到的xsrf为：",xsrf_token)

# 获取验证码
def get_captcha():
    t = str(int(time.time()) * 1000)
    captcha_url = "https://www.zhihu.com/captcha.gif?r=" + t + "&type=login"
    r = session.get(url=captcha_url,headers=headers)
    with open("captcha.jpg","wb") as f:
        f.write(r.content)
        f.close()
    im = Image.open("captcha.jpg")
    im.show()
    im.close()
    captcha = input("请输入验证码\n")
    return captcha

# 是否登录
def isLogin():
    setting_url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url=setting_url,headers=headers,allow_redirects=False).status_code
    if login_code == 200:
        return True
    else:
        return False

# 登录
def login(account, password):
    _xsrf = get_xsrf()
    headers["X-Xsrftoken"] = _xsrf
    headers["X-Requested-With"] = "XMLHttpRequest"

    if re.match(r"^1\d{10}$", account):
        print("手机号登录\n")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf":_xsrf,
            "password":password,
            "phone_num":account
        }
    else:
        if "@" in account:
            print("邮箱登录\n")
        else:
            print("输入账号有问题")
            return 0
        post_url = "https://www.zhihu.com/login/email"
        post_data = {
            "_xsrf": _xsrf,
            "password": password,
            "email": account
        }

    login_page = session.post(url=post_url,data=post_data,headers=headers)
    login_code = login_page.json()
    if login_code["r"] == 1:
        post_data["captcha"] = get_captcha()
        login_page = session.post(url=post_url,data=post_data,headers=headers)
        login_code = login_page.json()
        print(login_code["msg"])


if __name__ == "__main__":
    if isLogin():
        print("您已经登录")
    else:
        account = input("用户名\n")
        password = input("密码\n")
        login(account,password)
