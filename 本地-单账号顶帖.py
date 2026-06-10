# coding:utf-8
import requests
import time
import random
import urllib.parse
import os
import webbrowser
from hashlib import md5
from lxml import html

# ================= 配置区 =================
ID = "638009038" # 示例 https://movie.douban.com/review/17647190/- 此处填写17647190
ACCOUNTS = [
    {'cookie': '这里输入网页cookies', 'ck': '这里输入四位CK'},
]
CHAOJIYING_USER = "elmagnificocj"
CHAOJIYING_PASS = "elmagnifico93"
CHAOJIYING_SOFTID = "914754"

PARS = [
    "期待张泽禹在一路向海的少年里的精彩表现",
    "坐等开播！超级期待张泽禹的小舞台",
    "支持张泽禹的新节目，希望能看到不一样的精彩"
]

class Chaojiying_Client:
    def __init__(self, username, password, soft_id):
        self.username = username
        self.password = md5(password.encode('utf8')).hexdigest()
        self.soft_id = soft_id
        self.base_params = {'user': self.username, 'pass2': self.password, 'softid': self.soft_id}
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def PostPic(self, im):
        params = {'codetype': 1902}
        params.update(self.base_params)
        files = {'userfile': ('captcha.jpg', im)}
        try:
            r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers, timeout=10)
            return r.json()
        except: return {"err_no": -999}

def main_run(acc, cj):
    sess = requests.session()
    headers = {'User-Agent': 'Mozilla/5.0', 'Cookie': acc['cookie']}
    data = {'ck': acc['ck'], 'rv_comment': random.choice(PARS), 'submit_btn': '加上去'}
    
    url = f'https://movie.douban.com/subject/38500062/discussion/{ID}/add_comment'
    resp = sess.post(url, data=data, headers=headers)
    
    if "captcha_image" in resp.text:
        print("⚠️ 触发验证码！已自动为你打开图片...")
        img_url = "https:" + html.fromstring(resp.content).xpath("//img[@id='captcha_image']/@src")[0]
        cid = html.fromstring(resp.content).xpath("//input[@name='captcha-id']/@value")[0]
        
        img = requests.get(img_url, headers=headers).content
        with open("captcha.jpg", "wb") as f: f.write(img)
        webbrowser.open("captcha.jpg") # 自动弹窗查看验证码
        
        # 使用超级鹰识别
        res = cj.PostPic(img)
        sol = res.get('pic_str') if res.get('err_no') == 0 else ""
        
        sol = input(f"识别结果为 [{sol}]，请确认或手动输入验证码: ").strip() or sol
        
        data.update({'captcha-solution': sol, 'captcha-id': cid})
        resp = sess.post(url, data=data, headers=headers)
        
    if resp.status_code in [200, 302]:
        print(f"🎉 发布成功！")
    else:
        print(f"❌ 发布失败，状态码: {resp.status_code}")

# 启动
cj = Chaojiying_Client(CHAOJIYING_USER, CHAOJIYING_PASS, CHAOJIYING_SOFTID)
for i in range(200):#顶帖次数
    main_run(ACCOUNTS[0], cj)
    #间隔时间设置 请根据自身账号稳定程度设置 如需更改 务必先暂停运行
    wait = random.randint(60, 120)
    print(f"⏳ 等待 {wait} 秒后进行下一次...")
    time.sleep(wait)