
from src.pxCaptcha import captcha_bypass
from bs4 import BeautifulSoup
from src.const import ACCOUNTS_DATA, URL
from src.user import User
from src.user.components.Component import Component


class Address(Component):
    def __init__(self, session, user_id, logger):
        super().__init__(session, user_id, logger)

    @captcha_bypass
    def go_address_page(self):
        #TODO: look and try to do it with a unlogged session seems like INFINITE csrf api access
        res = self.session.get(URL + "/on/demandware.store/Sites-snse-SOUTH-Site/it_IT/Address-AddAddress?format=ajax", json=True)
        # csrf_token = res.json()["csrf"]["token"]
        # return csrf_token
        return res

    @captcha_bypass
    def verify_address(self, csrf_token):
        address_info = ACCOUNTS_DATA[self.user_id]["address"]
        address_info.update({"csrf_token": csrf_token})
        res = self.session.post(URL + "/on/demandware.store/Sites-snse-SOUTH-Site/it_IT/CheckoutAddressServices-Validate?format=ajax", data=address_info)
        return res

    @captcha_bypass
    def save_address(self, csrf_token):
        account_info = ACCOUNTS_DATA[self.user_id]
        address_info = ACCOUNTS_DATA[self.user_id]["address"]
        data = {
            "dwfrm_address_title": "Herr", # Only male
            "dwfrm_address_firstName": account_info["name"],
            "dwfrm_address_lastName": account_info["surname"],
            "dwfrm_address_postalCode": address_info["postalCode"],
            "dwfrm_address_city": address_info["city"],
            "dwfrm_address_street": address_info["street"],
            "dwfrm_address_suite": address_info["houseNo"],
            "dwfrm_address_address1": "",
            "dwfrm_address_address2": address_info["houseNo"],
            "dwfrm_address_phone": "",
            "dwfrm_address_countryCode": address_info["country"],
            "csrf_token": csrf_token
        }
        res = self.session.post(URL + "/on/demandware.store/Sites-snse-SOUTH-Site/it_IT/Address-SaveAddress?methodId=home-delivery_it&format=ajax", data=data, json=True)
        return res
    
    def register_address(self):
        res = self.go_address_page()
        soup = BeautifulSoup(res.text, "html.parser")
        csrf_token = soup.find("input", {"name":"csrf_token"})["value"]
        
        self.verify_address(csrf_token)
        return self.save_address(csrf_token)