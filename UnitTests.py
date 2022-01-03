
import unittest
from src.user import User

from src.user.components.login import Login
from src.const import ACCOUNTS_DATA
import random

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.user_id = random.choice(list(ACCOUNTS_DATA.keys()))
        self.login = Login(self.user_id)

    def test_login_json_response(self):
        res = self.login.login()
        self.assertIsInstance(res.json(), dict)

    def test_login_success(self):
        res = self.login.login()
        self.assertTrue(res.json()["success"], True)

class TestPXCaptcha(unittest.TestCase):
    def setUp(self):
        self.user_id = random.choice(list(ACCOUNTS_DATA.keys()))
        self.login = Login(self.user_id)

    def test_pxcaptcha_bypass(self):
        self.login.session.headers = {"User-Agent": "Googlebot-Image/1.0"} # Triggering bot system
        res = self.login.login()
        self.assertTrue(res.status_code, 200)

unittest.main()