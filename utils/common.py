import json
import sys
import os


def store_cookies(restore=False):
    """存储并返回 Cookie 字典"""

    def cookie_to_json():
        """将分号分隔的 Cookie 转为字典"""

        cookies_dict = {}
        raw_cookies = input('> ')
        if not raw_cookies:
            return {}
        if raw_cookies[:7].lower() == 'cookie:':
            raw_cookies = raw_cookies[7:]

        for cookie in raw_cookies.split(';'):
            key, value = cookie.lstrip().split("=", 1)
            cookies_dict[key] = value

        return cookies_dict

    file_path = os.path.join(sys.path[0], "cookies.json")
    if not os.path.isfile(file_path):
        cookies = {}
    else:
        with open(file_path, 'r') as cookies_file:
            cookies = json.load(cookies_file)

    if restore or not cookies:
        print("输入 Cookie：")
        cookies = cookie_to_json()
        with open(file_path, 'w') as f:
            json.dump(cookies, f, indent=2)

    return cookies
