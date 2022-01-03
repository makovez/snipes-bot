from requests import Session
from bs4 import BeautifulSoup
from src.const import URL, USER_AGENT
from src.pxCaptcha import captcha_bypass

ccsidFilter = lambda tag: tag.name == "span" and len(tag.attrs) == 2 and "data-value" in tag.attrs and "data-id" in tag.attrs

class Register:
    def __init__(self):
        self.session = Session()
        self.session.headers = {
            "User-Agent":USER_AGENT
        }   

    def go_register_page(self):
        res = self.session.get(URL + "/registration?rurl=1")

        soup = BeautifulSoup(res.text, "html.parser")
        ccsid_element = soup.find(ccsidFilter)
        csrf_token = soup.find("input", {"name":"csrf_token"})["value"]

        return {**ccsid_element.attrs, **{"csrf":csrf_token}}

    @captcha_bypass
    def submit_register(self, payload, email, password, name, surname):
        ccsid = self.session.cookies.pop("ccsid")
        if ccsid != payload["data-id"]: return -1 # Must match the cookie ccsid
        data = {
            ccsid: payload["data-value"], # ccsid:ccsid_value
            "dwfrm_profile_register_title": "Herr",
            "dwfrm_profile_register_firstName": name,
            "dwfrm_profile_register_lastName": surname,
            "dwfrm_profile_register_email": email,
            "dwfrm_profile_register_emailConfirm": email,
            "dwfrm_profile_register_password": password,
            "dwfrm_profile_register_passwordConfirm": password,
            "dwfrm_profile_register_phone": "",
            "dwfrm_profile_register_birthday": "",
            "dwfrm_profile_register_addToEmailList": True,
            "dwfrm_profile_register_acceptPolicy": True,
            "csrf_token": payload["csrf"]
        }
        res = self.session.post(URL + "/on/demandware.store/Sites-snse-SOUTH-Site/it_IT/Account-SubmitRegistration?rurl=1&format=ajax", data=data, json=True)
        return res

    def register(self, email, password, name, surname):
        payload = self.go_register_page()

        res = self.submit_register(payload, email, password, name, surname)
        return res.json()
