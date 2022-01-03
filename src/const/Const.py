import os
import json 
from collections import deque
class Proxy:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

URL = 'https://www.snipes.it'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

SESSIONS_PATH = os.path.join(os.getcwd(), "src", "saved_sessions")
JSON_ACCOUNT_PATH = os.path.join(os.getcwd(), "src", "accounts.json")
JS_PATH = os.path.join(os.getcwd(), "src", "js")
LOG_PATH = os.path.join(os.getcwd(), "src", "logs")
DRIVER_SELENIUM = os.path.join(os.getcwd(), "src", "mode", "restock", "gecko", "geckowin.exe")

MAX_PROXY_ROTATE = 5 # Max proxy rotate plan for scraping products 
PROXY_ROTATE = [Proxy("e1.p.webshare.io", "80", "user", "pwd") for x in range(1, MAX_PROXY_ROTATE + 1)]

MAX_PROXY_RESIDENTIALS = 20 # Max proxy for session users 
PROXY_RESIDENTIALS = [Proxy("e1.p.webshare.io", "80", "user", "pwd") for x in range(1, MAX_PROXY_RESIDENTIALS + 1)]

KEEP_ALIVE_SEC = 60.0 # Seconds to keep alive sessions

with open(JSON_ACCOUNT_PATH) as f:
    ACCOUNTS_DATA = json.load(f)

KEY_WORDS = ["nike dunk high", "university blue jordan 1", "Yeezy Boost 350"]
SIZES = [38.5, 42.5]


START_SESSIONS_MONITORS_SIZES = 2 # This good for watching 2 product for each keyword
RANDOM_PRODUCT = "/p/nike-air_force_1_lv8_-white%2Fmulticolor%2Fblack-00013801898088.html"
