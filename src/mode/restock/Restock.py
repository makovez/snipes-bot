from src.const.Const import PROXY_RESIDENTIALS, ACCOUNTS_DATA, KEEP_ALIVE_SEC, SIZES, RANDOM_PRODUCT
from src.user import User
from src.monitor.Monitor import product_sizes_link
import threading, logging, time, random, requests
from src.mode.restock.OpenSession import start_selenium_instance
class Restock:
    def __init__(self, user: User) -> None:
        self.user = user
        self.user_id = user.user_id
        self.logger = self.user.logger
        self.keep_alive() # Ensure session is always logged in 
        self.keep_ready_to_cart() # Ensure ready to cart
        self.done = False
    
    def keep_alive(self):
        self.logger.info("Keep alive")
        self.user.login() # Ensure logged in 
        t = threading.Timer(KEEP_ALIVE_SEC, self.keep_alive)
        t.daemon = True
        t.start()

    def keep_ready_to_cart(self):
        self.logger.info("Keep ready to cart")
        self.user.product.product_page(RANDOM_PRODUCT)
        t = threading.Timer(KEEP_ALIVE_SEC, self.keep_ready_to_cart)
        t.daemon = True
        t.start()

    def look_up(self):
                
        if not any(bool(x) for _, x in product_sizes_link.copy().items()):
            return None, None
        
        for psize in SIZES:
            for product, sizes_link in product_sizes_link.items():
                for size, size_link in sizes_link.items():
                    if str(psize) == size:
                        return product, size_link

        

        prod = random.choice(list(product_sizes_link.keys()))
        return prod, random.choice(list(product_sizes_link[prod].values()))
    
    def buy(self):
        while not self.done:
            prod, product_sizelink = self.look_up()
            if not product_sizelink: # Can't find still nothing
                continue

            self.logger.info(f"Trying to cart {prod}")

            res = self.user.add_cart_from_sizelink(product_sizelink, quantity="1") # Add to cart
            if res and not res["error"]: 
                self.logger.info("OK - Checkout")
                res = self.user.checkout() # Checkout item
                if not res["error"]:
                    self.logger.info("OK - success")
                    self.logger.info(res)
                    start_selenium_instance(self.user_id, res["continueUrl"])
                    for _ in range(3):
                        pass
                        #send to telegram maybe requests.get(f"")
                    #requests.get(f"")
                    self.done = True
                else:
                    self.logger.info("Error at checkout")
            else:
                self.logger.info("Error at carting")

            self.user.clean_cart() # Clean cart to be sure everything ok
            
            


def start_restock_session(account: dict):
    random.shuffle(PROXY_RESIDENTIALS)
    buy = Restock(User(account, PROXY_RESIDENTIALS.pop()))
    t = threading.Thread(target=buy.buy)
    t.daemon = True
    t.start()
    return t

