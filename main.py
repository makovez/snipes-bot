#for proxify everything
# import socket, socks
# socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, "localhost", 8000)
# socket.socket = socks.socksocket

from src.const import KEY_WORDS, ACCOUNTS_DATA
from src.monitor.Monitor import start_monitor
from src.mode.restock.Restock import start_restock_session
from src import logger
import time

for account in ACCOUNTS_DATA:
    if account == "07568192":
        print(account)
        start_restock_session(account)

for keyword in KEY_WORDS:
    start_monitor(keyword)

while 1:
    time.sleep(1)
