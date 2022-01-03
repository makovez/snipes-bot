from src.const.Const import Proxy, RANDOM_PRODUCT
from .session import Session
from .components.profile import Profile
from .components.login import Login
from .components.product import Product
from .components.checkout import Checkout
import time
from src.logger import get_logger


class User:
    def __init__(self, user_id: str = "", proxy: Proxy = None):
        """[User controlls class. You can do any of the methods listed.]

        Args:
            user_id ([str]): [user_id of the user which must exists in sessions folder]
        """
        self.user_id = user_id
        self.session = Session(user_id=user_id, proxy=proxy)
        self.logger = get_logger(user_id) # Get the logger initialized with current user_id
        
        self.initialize_objects() # Initialize objects
        self.logger.info("Session initialized")

    def login(self):
        """[Check if logged and user session already exists. if not will create 
        user session and/or login if logged out due to timeout of session cookies.]

        Returns:
            [True]: [logged in succesfully]
            [None]: [Error not json response]
        """
        login = Login(self.session, self.user_id, self.logger) 
        self.session.load_session() # Load session if exists

        if not self.session.check_session() or not self.profile.is_logged(): # Create session
            print("Session not found or logged out, login and saving new one...")
            result = login.login()
            if not result.json():
                self.logger.error(f"product.get_size_number returned a non-json: {result}")
                #TODO: Can print html response here
                return None
        return True
          

    def initialize_objects(self):
        """[Initiaize all the mother components of the bot]
        """
        self.profile = Profile(self.session, self.user_id, self.logger)
        self.product = Product(self.session, self.user_id, self.logger)
        self.order = Checkout(self.session, self.user_id, self.logger) 


    def add_cart(self, prod_link, quantity="1"):
        """[Cart product from link/pid. Will first go to product page, 
            then check sizes available and find the preferred one based on constants sizes.]

        Args:
            product_link ([str]): [product_link]

        Return: 
            [json] - [response from site ]
            [False] - [no sizes available]
            [None] - [no json response (Error because json is expected)]

        """
        size_link = self.product.get_preferred_size_link(prod_link)

        if not size_link:
            self.logger.info(f"No sizes available for {prod_link}")
            return False
        else:
            self.logger.info(f"Checking {size_link}")

        res = self.product.get_size_info(size_link)
        if not res.json():
            self.logger.error(f"product.get_size_number returned a non-json: {res}")
            #TODO: Can print html response here
            return None

        size = res.json()["product"]["custom"]["size"]
        pid = res.json()["product"]["id"]

        self.logger.info(f"Adding cart item: size {size}, pid {pid}")

        res = self.product.add_cart(pid, size, quantity=quantity)
        if not res.json():
            self.logger.error(f"product.add_cart returned a non-json {res}")
            #TODO: Can print html response here
            return None

        return res.json()


    def add_cart_from_sizelink(self, size_link, quantity="1"):
        """[Cart product from sizelink. Will first go to product page, 
            then check sizes available and find the preferred one based on constants sizes.]

        Args:
            size_link ([str]): [size_link]

        Return: 
            [json] - [response from site]
            [False] - [no sizes available]
            [None] - [no json response (Error because json is expected)]

        """

        self.logger.info(f"Checking {size_link}")

        res = self.product.get_size_info(size_link)
        if not res.json():
            self.logger.error(f"product.get_size_number returned a non-json {res}")
            #TODO: Can print html response here
            return None

        size = res.json()["product"]["custom"]["size"]
        pid = res.json()["product"]["id"]

        self.logger.info(f"Adding cart item: size {size}, pid {pid}")

        res = self.product.add_cart(pid, size, quantity=quantity)
        if not res.json():
            self.logger.error(f"product.add_cart returned a non-json {res}")
            #TODO: Can print html response here
            return None

        return res.json()

    
    def clean_cart(self):
        """[Clean all cart items]

        Returns:
            [True]: [success]
            [None]: [error not json response]
        """
        self.product.product_page(RANDOM_PRODUCT) # Necessary to set cookie
        res = self.product.add_cart("", 0)
        if not res.json():
            self.logger.error(f"product.add_cart returned a non-json {res}")
            #TODO: Can print html response here
            return None
        self.logger.info("cleaning cart")
        for item in res.json()["cart"]["items"]:
            pid, uuid = item["id"], item["UUID"]
            res = self.product.remove_item(pid, uuid)
            if not res.json():
                self.logger.error(f"product.add_cart returned a non-json {res}")
                #TODO: Can print html response here
                return None
            self.logger.info(f"removed item: pid {pid}, uuid {uuid}")
            time.sleep(2)

        return True

    def checkout(self):
        """[Place order and checkout]

        Returns:
            [json]: [json response from the site]
            [None]: [no json response (Error because json is expected)]
        """
        res = self.order.place_order()
        if not res.json():
            self.logger.error(f"product.add_cart returned a non-json {res}")
            #TODO: Can print html response here
            return None
        return res.json()


