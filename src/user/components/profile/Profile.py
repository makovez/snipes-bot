from src.user import User
from src.const import ACCOUNTS_DATA, URL
from src.pxCaptcha import captcha_bypass
from src.user.components.Component import Component
from .Address import Address

class Profile(Component):
    def __init__(self, session, user_id, logger):
        super().__init__(session, user_id, logger)
        self.address = Address(session, user_id, logger)

    @captcha_bypass
    def _go_profile_page(self):
        """go profile page
        """
        res = self.session.get(URL + "/view-account?registration=false")
        return res

    def is_logged(self) -> bool:
        """Check if logged in by looking for user_id in html page

        Returns:
            bool: [false / true]
        """
        res = self._go_profile_page()
        return (self.user_id in res.text)

    """def register_address(self):
        return self.address.register_address()"""

# p = Profile("07802111")
# p.register_address()


# {\n  "action": "Address-SaveAddress",\n  "queryString": "format=ajax&methodId=home-delivery_it",\n  "locale": "it_IT",\n  "loggedin": true,\n  "success": true\n}