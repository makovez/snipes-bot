
import time, random, requests, os, logging

from py_mini_racer.py_mini_racer import MiniRacer
from capmonster_python import NoCaptchaTaskProxyless
from requests.api import get

from src.const.Const import JS_PATH


JS_MODULES = ["payloadEncode.js", "pc.js", "uuid.js"]
CTX = MiniRacer()

def laod_module(name):
    with open(os.path.join(JS_PATH, name), "r") as f:
        CTX.eval(f.read())

for module_name in JS_MODULES:
    laod_module(module_name)
class PxCaptcha:
    def __init__(self):
        self.ctx = CTX
        self.uuid = self.ctx.call("vt")
        self.p = self.uuid + ":v6.4.3:196"
    
    def create_payload(self, page_link, recaptcha):
        random_value = random.randint(555, 4444)
        start_time = int(round(time.time() * 1000))
        px_parameters = [
            {
                "t":"PX761",
                "d":
                {
                    "PX70":random_value,
                    "PX34":"TypeError: Cannot read property '0' of null\n    at On (https://client.perimeterx.net/PX7nhy00fz/main.min.js:2:14650)\n    at fe (https://client.perimeterx.net/PX7nhy00fz/main.min.js:2:27962)\n    at Object.qt [as PX763] (https://client.perimeterx.net/PX7nhy00fz/main.min.js:2:26645)\n    at o (https://captcha.px-cdn.net/PX7nhy00fz/captcha.js?a=c&amp;u=14b05d50-866a-11eb-8a3d-e5dbdabbc73f&amp;v=&amp;m=0:3:50993)\n    at window.<computed> (https://captcha.px-cdn.net/PX7nhy00fz/captcha.js?a=c&amp;u=14b05d50-866a-11eb-8a3d-e5dbdabbc73f&amp;v=&amp;m=0:3:53334)\n    at C7.cT.P (https://www.gstatic.com/recaptcha/releases/6g5J7UfDQ9mLrweZHj04ekSP/recaptcha__en_gb.js:670:46)\n    at Q.Y (https://www.gstatic.com/recaptcha/releases/6g5J7UfDQ9mLrweZHj04ekSP/recaptcha__en_gb.js:252:98)\n    at new Promise (<anonymous>)\n    at J8.Y (https://www.gstatic.com/recaptcha/releases/6g5J7UfDQ9mLrweZHj04ekSP/recaptcha__en_gb.js:252:70)\n    at Array.<anonymous> (https://www.gstatic.com/recaptcha/releases/6g5J7UfDQ9mLrweZHj04ekSP/recaptcha__en_gb.js:195:445)",
                    "PX1129":True,
                    "PX1130":False,
                    "PX610":True,
                    "PX754":False,
                    "PX755":recaptcha,
                    "PX756":"reCaptcha",
                    "PX757":"www.snipes.it",
                    "PX850":1,
                    "PX851":random_value + random.randint(55, 444),
                    "PX1056":start_time,
                    "PX1038":self.uuid,
                    "PX371":False,
                    "PX250":"PX557",
                    "PX708":"c",
                    "PX96":page_link
                }
            }
        ]

        return str(px_parameters).replace("'", '"').replace('"0"', "'0'").replace("False", "false").replace("True", "true")

    def encode_payload(self, payload):
        return self.ctx.call("encodePayload", payload)

    def pc(self, payload):
        return self.ctx.call("Zn", payload, self.p)

    def data_payload(self, encoded_payload, pc, pxhd):
        data = {
            "payload": encoded_payload,
            "appId": "PX7nhy00fz",
            "tag": "v6.4.3",
            "uuid": self.uuid,
            "ft": 196,
            "seq": 1,
            "en": "NTA",
            "pc": pc,
            "pxhd": pxhd, # Froom cookie,
            "rsc":12
        }

        return data

capmonster = NoCaptchaTaskProxyless(client_key="PUT YOUT KEY") # capmonster.cloud
def get_recaptcha():
    taskId = capmonster.createTask(website_key="6LckWxMaAAAAAFNKJngAwL5pktTsG4-NiSvcYktS", website_url="https://www.snipes.it/")
    response = capmonster.joinTaskResult(taskId=taskId)
    return response

def captcha_bypass(func):
    def wrapper(self, *arg, **kw):            
        res = func(self, *arg, **kw)
        if res.status_code == 403:

            if "_pxhd" not in res.cookies:
                print("_pxhd cookie not found, trying again...")
                return wrapper(self, *arg, **kw)
                
            px = PxCaptcha()
            self.logger.info("Captcha detected, bypassing..")
            pxhd = res.cookies["_pxhd"]
            
            recaptcha = get_recaptcha()

            payload = px.create_payload(res.url, recaptcha)
            encode_payload = px.encode_payload(payload)
            pc = px.pc(payload)

            data_payload = px.data_payload(encode_payload, pc, pxhd)
            requests.post("https://collector-px7nhy00fz.px-client.net/assets/js/bundle", data=data_payload)
                
            return wrapper(self, *arg, **kw)

        return res
    return wrapper
