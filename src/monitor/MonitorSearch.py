import time, threading
from bs4 import BeautifulSoup
from src.pxCaptcha.PxCaptcha import captcha_bypass
from src.const.Const import URL
from src.user import User
from src.logger import get_logger

class MonitorSearch:
    def __init__(self, session, keyword):
        """Load session from user_id

        Args:
            user_id (str): [user_id from snipes]
        """
        self.session = session
        self.keyword = keyword
        self.available_products = []
        self.logger = get_logger("monitor-search" + " " + keyword)
        

    @captcha_bypass
    def search_page(self):
        res = self.session.get(URL + f"/search?q={self.keyword}&lang=it_IT")
        return res

    def search(self):
        res = self.search_page()
        if URL + "/p/" in res.url: # The site redirects directly to product page if one size found
            return [res.url.replace(URL, "")]
        soup = BeautifulSoup(res.text, 'html.parser')
        products = soup.find_all("a", {"class":"b-product-tile-body-link"})
        return [prod["href"] for prod in products]


    def run(self):
        prods = self.search()
        if prods:
            self.logger.info(f"Found {len(prods)} products")
        for product in prods:
            if product not in self.available_products:
                self.available_products.append(product)
        
        t = threading.Timer(3, self.run)
        t.daemon = True
        t.start()
    
    def get_available_products(self):
        return self.available_products




