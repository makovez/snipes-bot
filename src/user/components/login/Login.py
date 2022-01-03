import logging
from bs4 import BeautifulSoup
from src.const import URL, ACCOUNTS_DATA
from src.pxCaptcha import captcha_bypass
from src.user import User
from src.user.session import save_cookie
from src.user.components.Component import Component

ccsidFilter = lambda tag: tag.name == 'span' and len(tag.attrs) == 2 and 'data-value' in tag.attrs and 'data-id' in tag.attrs

class Login(Component):

    def __init__(self, session, user_id, logger):
        super().__init__(session, user_id, logger)
        self.email = ACCOUNTS_DATA[self.user_id]["email"]
        self.password = ACCOUNTS_DATA[self.user_id]["password"]
        
    @captcha_bypass
    def go_login_page(self):
        """Go to login page and retrieve page

        Returns:
            [res]: [res html]
        """
        res = self.session.get(URL + '/login')
        return res

    @captcha_bypass
    def submit_login(self, payload):
        """Login user

        Args:
            payload ([type]): [ccsid, ccsid_value, csrf]

        Returns:
            [string]: [user_id]
        """

        if 'ccsid' in self.session.cookies: # sometimes doesen't appears in cookiesbut only in html
            self.session.cookies.pop('ccsid')

        ccsid = payload['data-id']

        data = {
            ccsid: payload['data-value'], 
            'dwfrm_profile_customer_email': self.email, 
            'dwfrm_profile_login_password': self.password, 
            'dwfrm_profile_login_rememberme': 'true', 
            'csrf_token': payload['csrf']
        }
        res = self.session.post(URL + '/authentication?rurl=1&format=ajax', data=data, json=True)
        return res

    @save_cookie
    def login(self):
        """[Login and return json res]
        """
        res = self.go_login_page()

        if 'ccsid' not in self.session.cookies: # sometimes doesen't appears in cookies but only in html
            logging.debug("submit_login - ccsid not in cookies")
            #TODO: dump page and res.cookies

        soup = BeautifulSoup(res.text, 'html.parser')
        ccsid_element = soup.find(ccsidFilter)
        csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
        payload = {**(ccsid_element.attrs), **{'csrf': csrf_token}}

        res = self.submit_login(payload)
        return res






