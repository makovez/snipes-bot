from queue import Queue
import time, threading, random, itertools
from bs4 import BeautifulSoup
from requests.api import get
from src.pxCaptcha.PxCaptcha import captcha_bypass
from src.const.Const import PROXY_ROTATE, URL, START_SESSIONS_MONITORS_SIZES, RANDOM_PRODUCT
from src.user.session import Session
from src.user.components.product.Product import Product
from src.logger import get_logger
class SessionDispatcher:
    def __init__(self, sessions):
        self.count = 0
        self.sessions = itertools.cycle(sessions)
        self.current = next(self.sessions)

    def __iter__(self):
        return self

    def __next__(self): # Python 2: def next(self)
        self.count += 1
        if self.count < 20: # Not over max
            return self.current
        
        self.current = next(self.sessions) # Set next as current session
        self.count = 0 # Reset count 
        return self.current

class MonitorSizes:
    def __init__(self, product_sizes_link: dict, keyword):
        """Load session from user_id

        Args:
            user_id (str): [user_id from snipes]
        """
        self.product_sizes_link = product_sizes_link
        self.keyword = keyword
        self.logger = get_logger("monitor-sizes" + " " + keyword)
        self.sessions = self.gen_session_iterator()

    def gen_session_iterator(self):
        sessions = []
        self.logger.info("Generating monitor size sessions...")

        def start_session():
            session = Session(proxy=random.choice(PROXY_ROTATE))
            session.set_bot_user() # Trigger captcha
            self.product_page(session, RANDOM_PRODUCT) #TODO: random product
            session.set_normal_user()
            sessions.append(session)

        for _ in range(2*START_SESSIONS_MONITORS_SIZES):
            t = threading.Thread(target=start_session)
            t.daemon = True
            t.start()
        
        while len(sessions) < 2*START_SESSIONS_MONITORS_SIZES:
            time.sleep(1)

        self.logger.info("Monitor size sessions generated")
        return SessionDispatcher(sessions)


    @captcha_bypass
    def product_page(self, session, product_link):
        """[Go to product page]

        Args:
            product_link ([string]): [product link: ex. "/p/shoes.html"]

        Returns:
            [html]: [the page of the product]
        """
        res = session.get(URL + product_link)
        return res


    def get_sizes_link(self, session, product_link):
        """[Go to product page and get size_links for the available sizes]

        Args:
            product_link ([type]): [description]

        Returns:
            [type]: [description]
        """
        res = self.product_page(session, product_link)
        soup = BeautifulSoup(res.text, "html.parser")
        elements = soup.find_all("a", {"data-attr-id":"size"})

        product_sizes_link = {}
        for elem in elements:
            if ("b-swatch-value--orderable" in elem.span["class"]):
                product_sizes_link.update({elem.span["data-attr-value"]:elem["data-href"]})

        return product_sizes_link

    def find_sizes(self, product_link):
        while True:
            res = self.get_sizes_link(next(self.sessions), product_link)
            self.logger.debug(f"Found size {product_link}: {len(res)}")
            self.product_sizes_link.update({product_link: res})
            time.sleep(1.5)


    def start_find_sizes(self, product_link):
        t = threading.Thread(target=self.find_sizes, args=(product_link,))
        t.daemon = True
        t.start()
        return t

        
