# import socket
# import time


# server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
# # server.bind(("::1", 50000))
# server.bind(("fd04:2240::1cef", 50000))
# server.listen()

# (conn, address) = server.accept()

# while True:
#     time.sleep(1)


import socket
import socketserver


class TCPServer6(socketserver.TCPServer):
    address_family = socket.AF_INET6
    # def __init__(self, *args):
    #     super().__init__(*args)
        # self.address_family = socket.AF_INET6


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        pieces = [b'']
        total = 0
        while b'\n' not in pieces[-1] and total < 10_000:
            pieces.append(self.request.recv(2000))
            total += len(pieces[-1])
        self.data = b''.join(pieces)
        print(f"Received from {self.client_address[0]}:")
        print(self.data.decode("utf-8"))
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
        # after we return, the socket will be closed.

if __name__ == "__main__":
    # HOST, PORT = "fd04:2240::1cef", 50000
    HOST, PORT = "::", 50000

    # Create the server, binding to localhost on port 9999
    with TCPServer6((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
