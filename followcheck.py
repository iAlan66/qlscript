import requests
import json
import os
import logging
import io

from notify import send

"""
follow 青龙面板签到脚本

需要手动在浏览器获取 csrf 和 cookie，然后填入环境变量，FOLLOW_CSRF 和 FOLLOW_COOKIE。

"""
'''
cron: 0 0 10 * * ?
new Env("Follow签到")
'''

# 创建 StringIO 对象
log_stream = io.StringIO()

# 配置 logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建控制台 Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# 创建 StringIO Handler
stream_handler = logging.StreamHandler(log_stream)

# 将两个 Handler 添加到 logger
logger.addHandler(console_handler)
logger.addHandler(stream_handler)

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
        logger.info(response_message)
    else:
        logger.error(response_message)

if __name__ == '__main__':
    if CSRF is None or COOKIE is None:
        error_message = "CSRF or COOKIE is None"
        logger.error(error_message)
        send(error_message)
        raise Exception("CSRF or COOKIE is None")
    checkin(CSRF, COOKIE)