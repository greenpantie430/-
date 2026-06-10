
# Online Python - IDE, Editor, Compiler, Interpreter

# coding:utf-8
import requests
import time
import random
import os
import webbrowser
from hashlib import md5

# ================= 配置区 =================
ID = "38500062"  # 示例 https://movie.douban.com/review/17647190/- 此处填写17647190
ACCOUNTS = [
    {'cookie': '这里输入网页cookies', 'ck': '这里输入四位CK'},
    {'cookie': '这里输入网页cookies', 'ck': '这里输入四位CK'},
]
PARS = ["期待张泽禹在一路向海的少年里的精彩表现", "坐等开播！超级期待张泽禹的小舞台", "支持张泽禹的新节目", "一路向海的少年，张泽禹冲呀！"]

# ================= 核心逻辑 =================
def main_run(acc, idx):
    sess = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': acc['cookie'],
        'Referer': f'https://movie.douban.com/subject/38500062/discussion/{ID}/'
    }
    data = {'ck': acc['ck'], 'rv_comment': random.choice(PARS), 'submit_btn': '加上去'}

    try:
        resp = sess.post(f'https://movie.douban.com/subject/38500062/discussion/{ID}/add_comment', data=data, headers=headers)
        
        # 判断是否触发验证码
        if "captcha_image" in resp.text:
            print(f"⚠️ [账号{idx}] 触发验证码！")
            # 简单逻辑：如果本地触发，提醒你去浏览器处理或查看验证码
            print("请检查你的网页端是否弹出验证码，或者手动在浏览器完成验证后重试。")
            
        elif resp.status_code in [200, 302]:
            print(f"🎉 [账号{idx}] 发布成功! 文案: {data['rv_comment']}")
        else:
            print(f"❌ [账号{idx}] 发布失败，状态码: {resp.status_code}")
            
    except Exception as e:
        print(f"⚠️ 网络连接异常: {e}")

# 启动循环
for i in range(200):
    main_run(ACCOUNTS[i % len(ACCOUNTS)], (i % len(ACCOUNTS)) + 1)
    
    # 间隔时间设置 请根据自身账号稳定程度设置 如需更改 务必先暂停运行
    wait_time = random.randint(60, 120)
    print(f"⏳ 等待 {wait_time} 秒后进行下一次...")
    time.sleep(wait_time)
    print("-" * 30)