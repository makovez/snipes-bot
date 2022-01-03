from typing import Dict
from src.pxCaptcha import captcha_bypass
from src.user import User
from src.const.Const import Proxy, USER_AGENT, PROXY_ROTATE, KEY_WORDS
from src.const import URL
from bs4 import BeautifulSoup
import threading, time, queue, random

from .MonitorSizes import MonitorSizes
from .MonitorSearch import MonitorSearch

product_sizes_link = {}
class Monitor(User):
    def __init__(self, keyword, proxy: Proxy = None):
        super().__init__(proxy=proxy, user_id=keyword)
        self.keyword = keyword
        self.msearch = None
        self.active_threads: Dict[str, threading.Thread] = dict()
        self.msizes = None

    def run(self):
        self.msearch = MonitorSearch(self.session, keyword=self.keyword)
        self.msizes = MonitorSizes(product_sizes_link, keyword=self.keyword)

        self.msearch.run() # Start thread monitor search
        while True:
            products_available = self.msearch.get_available_products() # Get updates from search
            
            # Add a sizes montior for each product
            for product in products_available: 
                if product not in self.active_threads:
                    thread = self.msizes.start_find_sizes(product) # Start thread
                    self.active_threads[product] = thread
                    
            
            # Stop size monitor if can't find anymore in search the product
            for product, thread in self.active_threads.items():
                if product not in products_available:
                    thread.stop()
                    
            time.sleep(1)


def start_monitor(keyword):
    random.shuffle(PROXY_ROTATE)
    t = threading.Thread(target=Monitor(keyword, proxy=PROXY_ROTATE[0]).run)
    t.daemon = True
    t.start()
    return t