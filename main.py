# import socket
import time

from server import MyServer


# server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
# # server.bind(("::1", 50000))
# server.bind(("fd04:2240::1cef", 50000))
# server.listen()

# (conn, address) = server.accept()

# while True:
#     time.sleep(1)


import signal


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    server.shutdown()








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

myserver = MyServer(host="::", port=50000)
myserver.start()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        myserver.teardown()
        break
