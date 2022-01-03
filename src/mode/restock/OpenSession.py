import pickle, os
import selenium.webdriver
from src.const.Const import URL, SESSIONS_PATH, DRIVER_SELENIUM


def start_selenium_instance(user_id, payment_page):
    driver = selenium.webdriver.Firefox(executable_path=DRIVER_SELENIUM)
    driver.get(URL)
    cookies = pickle.load(open(os.path.join(SESSIONS_PATH, user_id), "rb"))
    for cookie in cookies:
        print(cookie.name, cookie.value)
        driver.add_cookie(
            {
                "name": cookie.name,
                "value": cookie.value
            }
        )
    driver.get(payment_page)


