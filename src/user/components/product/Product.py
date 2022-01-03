from bs4 import BeautifulSoup
from src.user.components import Component
from src.user import User
from src.user.session import save_cookie

from src.const import URL, SIZES
from src.pxCaptcha import captcha_bypass
import random

class Product(Component):
    def __init__(self, session, user_id, logger):
        super().__init__(session, user_id, logger)

    @save_cookie
    @captcha_bypass
    def product_page(self, product_link):
        """[Go to product page]

        Args:
            product_link ([string]): [product link: ex. "/p/shoes.html"]

        Returns:
            [html]: [the page of the product]
        """
        res = self.session.get(URL + product_link)
        return res


    def get_sizes_link(self, product_link):
        """[Go to product page and get size_links for the available sizes]

        Args:
            product_link ([type]): [description]

        Returns:
            [type]: [description]
        """
        res = self.product_page(product_link)
        soup = BeautifulSoup(res.text, "html.parser")
        elements = soup.find_all("a", {"data-attr-id":"size"})

        sizes_link = {}
        for elem in elements:
            if ("b-swatch-value--orderable" in elem.span["class"]):
                sizes_link.update({elem.span["data-attr-value"]:elem["data-href"]})

        return sizes_link

    
    def get_preferred_size_link(self, product_link):
        """[Get shoes size_link from preferred size otherwise random]

        Args:
            product_link ([str]): [link of the shoes page]

        Returns:
            [str]: [size_link]
        """
        sizes_link = self.get_sizes_link(product_link)
        if not sizes_link:
            return None # No sizes available

        for psize in SIZES:
            for size, link in sizes_link.items():
                if str(psize) == size:
                    return link
        
        return random.choice(list(sizes_link.values()))

    @captcha_bypass
    def get_size_info(self, size_link):
        """[Get the size info json page for the current size_link -> here ther's pid and other info]

        Args:
            size_link ([type]): [description]

        Returns:
            [json]: [json respoonse with size info]
        """
        res = self.session.get(URL + size_link + "&format=ajax")
        return res

    @captcha_bypass
    def add_cart(self, pid, size, quantity="1"):
        """[Add the product to the cart from pid and size]

        Args:
            pid ([string]): [The number identifying the shoes]
            size ([number]): [The size of the shoes]
            quantity (str, optional): [description]. Defaults to "1".

        Returns:
            [json]: [Return the json response from adding to cart]
        """
        data = {
            "pid": pid,
            "options": '[{"optionId":"212","selectedValueId":"%s"}]' % size,
            "quantity": quantity
        }
        res = self.session.post(URL + "/on/demandware.store/Sites-snse-SOUTH-Site/it_IT/Cart-AddProduct?format=ajax", data=data)
        return res

    @captcha_bypass
    def remove_item(self, pid, uuid):
        """[Remove item from pid and uuid]

        Args:
            pid ([string]): [The number identifying the shoes]
            uuid ([type]): [description]

        Returns:
            [json]: [Return the json response from removing shoes from cart]
        """
        res = self.session.get(URL + f"/on/demandware.store/Sites-snse-SOUTH-Site/it_IT/Cart-RemoveProductLineItem?format=ajax&pid={pid}&uuid={uuid}")
        return res
    
