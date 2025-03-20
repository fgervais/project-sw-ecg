# import socket
import logging
import signal
import time

from server import MyServer


# Used by docker-compose down
def sigterm_handler(signal, frame):
    global teardown

    logger.info("💥 Reacting to SIGTERM")
    teardown = True


logging.basicConfig(
    format="[%(asctime)s] %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

signal.signal(signal.SIGTERM, sigterm_handler)

myserver = MyServer(host="::", port=50000)
myserver.start()

teardown = False

while True:
    if teardown:
        myserver.teardown()
        break

    time.sleep(1)
