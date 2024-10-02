import requests
import json
import os
import logging

"""
follow 青龙面板签到脚本

需要手动在浏览器获取 csrf 和 cookie，然后填入环境变量，FOLLOW_CSRF 和 FOLLOW_COOKIE。

"""
'''
cron: 0 0 10 * * ?
new Env("Follow签到")
'''

# 环境变量获取csrf和cookie
CSRF = os.getenv("FOLLOW_CSRF")
COOKIE = os.getenv("FOLLOW_COOKIE")

def checkin(csrf, cookie):
    url = "https://api.follow.is/wallets/transactions/claim_daily"
    data = {
        "csrf": CSRF
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/4G Language/zh_CN",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cookie": COOKIE
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    response_code = response.json().get("code")
    response_message = response.json().get("message")
    if response_code == 2000:
        logging.info(response_message)
    else:
        logging.error(response_message)

if __name__ == '__main__':
    if CSRF is None or COOKIE is None:
        logging.error("CSRF or COOKIE is None")
        raise Exception("CSRF or COOKIE is None")
    checkin(CSRF, COOKIE)