# import socket
import logging
import signal
import time

import interface

from server_coap import CoAPServer


# Used by docker-compose down
def sigterm_handler(signal, frame):
    logger.info("💥 Reacting to SIGTERM")


logging.basicConfig(
    format="[%(asctime)s] %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

signal.signal(signal.SIGTERM, sigterm_handler)

dashboard = interface.Dashboard()

server = CoAPServer(dashboard)
server.start()

interface.exec()

server.stop()
server.join()
