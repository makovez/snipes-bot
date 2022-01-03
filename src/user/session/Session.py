
import pickle, os

from requests.sessions import default_headers
from src.const.Const import Proxy
from src.const import SESSIONS_PATH
from src.const import USER_AGENT
from requests import Session
from simplejson.errors import JSONDecodeError

def save_cookie(func):
    def wrapper(self, *arg, **kw):            
        res = func(self, *arg, **kw)
        print("Saving cookies...")
        self.session.save_session()
        return res
    return wrapper


class MySession(Session):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def request(self, *args, **kwargs):
        res = super().request(*args, **kwargs)
        json = res.json
        def wrapper():
            try:
                return json()
            except JSONDecodeError:
                return None
        res.json = wrapper
        return res

class Session(MySession):

    def __init__(self, user_id: str = None, proxy: Proxy = None):
        super().__init__()

        if proxy: self.set_proxy(proxy)
        
        self.headers = {'User-Agent': USER_AGENT}
        self.user_id = user_id
        self.loaded = False

    def set_normal_user(self):
        self.headers = {'User-Agent': USER_AGENT}

    def set_bot_user(self):
        self.headers = {'User-Agent': "Googlebot"}

    def set_proxy(self, proxy):
        self.proxies = {
            "http": f"http://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.port}",
            "https": f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.port}"
        }


    def save_session(self):
        """[Save session cookies to file]

        Args:
            user_id ([string]): [user_id of snipes]
            cookies : [Cookies from session]
        """
        if self.user_id: # Check if not empty aka normal empty session
            with open(os.path.join(SESSIONS_PATH, self.user_id), 'wb') as f:
                pickle.dump(self.cookies, f)

    def load_session(self):
        """Load session cookies from session user_id name if no previously loaded

        Args:
            user_id ([string]): [user_id of snipes]

        Returns:
            [cookies]: [Cookies saved from session]
        """

        if not self.loaded and self.check_session():
            with open(os.path.join(SESSIONS_PATH, self.user_id), 'rb') as f:
                self.cookies.update(pickle.load(f)) 
                self.loaded = True

    def check_session(self):
        return os.path.exists(os.path.join(SESSIONS_PATH, self.user_id))
    
    def __del__(self):
        self.close()
