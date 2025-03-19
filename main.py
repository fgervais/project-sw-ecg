# import socket
import logging
import signal
import time

from server import MyServer


# server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
# # server.bind(("::1", 50000))
# server.bind(("fd04:2240::1cef", 50000))
# server.listen()

# (conn, address) = server.accept()

# while True:
#     time.sleep(1)


# def signal_handler(sig, frame):
#     print("You pressed Ctrl+C!")
#     server.shutdown()



# Used by docker-compose down
def sigterm_handler(signal, frame):
    global teardown

    logger.info("💥 Reacting to SIGTERM")
    teardown = True






        # print(self.data.decode("utf-8"))
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
        # after we return, the socket will be closed.


# signal.signal(signal.SIGINT, signal_handler)

# HOST, PORT = "fd04:2240::1cef", 50000


# server = TCPServer6((HOST, PORT), MyTCPHandler)
# try:
#     server.serve_forever()
# except KeyboardInterrupt:
#     pass

# server.server_close()



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
