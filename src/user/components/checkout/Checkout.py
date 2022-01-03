from src.user import User
from bs4 import BeautifulSoup
from src.const import ACCOUNTS_DATA, URL
from src.pxCaptcha import captcha_bypass
from src.user.components.Component import Component
from src.user.session import save_cookie

class Checkout(Component):
    def __init__(self, session, user_id, logger):
        super().__init__(session, user_id, logger)
    
    @captcha_bypass
    @save_cookie
    def go_checkout_page(self):
        res = self.session.get(URL + "/checkout")
        return res

    @captcha_bypass
    @save_cookie
    def get_addresses(self):
        res = self.session.get(URL + "/addresses?format=ajax")
        return res

    @captcha_bypass
    @save_cookie
    def checkout_address(self, payload):
        account_info = ACCOUNTS_DATA[self.user_id]
        address_info = ACCOUNTS_DATA[self.user_id]["address"]

        payload.update({
            "dwfrm_shipping_shippingAddress_shippingMethodID":"home-delivery_it",
            "dwfrm_shipping_shippingAddress_addressFields_title":"Herr",
            "dwfrm_shipping_shippingAddress_addressFields_firstName":account_info["name"],
            "dwfrm_shipping_shippingAddress_addressFields_lastName":account_info["surname"],
            "dwfrm_shipping_shippingAddress_addressFields_postalCode":address_info["postalCode"],
            "dwfrm_shipping_shippingAddress_addressFields_city":address_info["city"],
            "dwfrm_shipping_shippingAddress_addressFields_street":address_info["street"],
            "dwfrm_shipping_shippingAddress_addressFields_suite":address_info["houseNo"],
            "dwfrm_shipping_shippingAddress_addressFields_address1":address_info["street"],
            "dwfrm_shipping_shippingAddress_addressFields_address2":address_info["houseNo"],
            "dwfrm_shipping_shippingAddress_addressFields_phone":account_info["phone"],
            "dwfrm_shipping_shippingAddress_addressFields_countryCode":address_info["country"],
            "dwfrm_billing_billingAddress_addressFields_title":"Herr",
            "dwfrm_billing_billingAddress_addressFields_firstName":account_info["name"],
            "dwfrm_billing_billingAddress_addressFields_lastName":account_info["surname"],
            "dwfrm_billing_billingAddress_addressFields_postalCode":address_info["postalCode"],
            "dwfrm_billing_billingAddress_addressFields_city":address_info["city"],
            "dwfrm_billing_billingAddress_addressFields_street":address_info["street"],
            "dwfrm_billing_billingAddress_addressFields_suite":address_info["houseNo"],
            "dwfrm_billing_billingAddress_addressFields_address1":address_info["street"],
            "dwfrm_billing_billingAddress_addressFields_address2":address_info["houseNo"],
            "dwfrm_billing_billingAddress_addressFields_countryCode":address_info["country"],
            "dwfrm_billing_billingAddress_addressFields_phone":account_info["phone"],
            "dwfrm_contact_email":account_info["email"],
            "dwfrm_contact_phone":account_info["phone"]
        })
        res = self.session.post(URL + "/on/demandware.store/Sites-snse-SOUTH-Site/it_IT/CheckoutShippingServices-SubmitShipping?format=ajax", data=payload)
        return res

    @captcha_bypass
    @save_cookie
    def checkout_payment(self, csrf_token):
        payload = {
            "dwfrm_billing_paymentMethod":"CREDIT_CARD",
            "dwfrm_giftCard_cardNumber": "",
            "dwfrm_giftCard_pin": "",
            "csrf_token":csrf_token
        }
        res = self.session.post(URL + "/on/demandware.store/Sites-snse-SOUTH-Site/it_IT/CheckoutServices-SubmitPayment?format=ajax", data=payload)
        return res

    @captcha_bypass
    @save_cookie
    def checkout_order(self):
        res = self.session.post(URL + "/on/demandware.store/Sites-snse-SOUTH-Site/it_IT/CheckoutServices-PlaceOrder?format=ajax")
        return res

    def place_order(self):
        res = self.go_checkout_page() # Go to checkout page to retrieve the payload 
        soup = BeautifulSoup(res.text, 'html.parser')

        try:
            payload = {
                "originalShipmentUUID": soup.find("input", {"name":"originalShipmentUUID"})["value"],
                "shipmentUUID": soup.find("input", {"name":"shipmentUUID"})["value"], 
                "address-selector": soup.find("input", {"class":"js-shipment f-native-radio-input"}, {"name": "address-selector"})["value"],
                "csrf_token": soup.find('input', {'name': 'csrf_token'})['value']
            }
        except Exception as e:
            print("Error at parsing checkout page: ", e)
            print("Trying again")
            return self.place_order()

        self.checkout_address(payload) # Checkout address
        self.checkout_payment(payload["csrf_token"]) # Checkout payment

        return self.checkout_order() # Place order

# c = Checkout("07802111")
# c.place_order()
