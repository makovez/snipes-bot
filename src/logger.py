import logging, os, sys
from datetime import datetime
from src.const import LOG_PATH

now = datetime.now().strftime("%m-%d-%Y_%H-%M-%S") # current date and time
logger_default = logging.getLogger()

def my_handler(type, value, tb):
    logger_default.exception("Uncaught exception: {0}".format(str(value)), extra={"user_id": "Exception"})

# Install exception handler
sys.excepthook = my_handler

ch = logging.StreamHandler()
fh = logging.FileHandler(os.path.join(LOG_PATH, f"debug_{now}.log"))
ch.setFormatter(logging.Formatter('%(levelname)s: [%(user_id)s] %(asctime)s\n%(message)s\n'))
fh.setFormatter(logging.Formatter('%(levelname)s: [%(user_id)s] %(asctime)s\n%(message)s\n'))

logging.basicConfig( level=logging.INFO, handlers=[ch, fh] )


def get_logger(user_id):
    logger = logging.LoggerAdapter(logger_default, extra={"user_id":user_id})
    return logger