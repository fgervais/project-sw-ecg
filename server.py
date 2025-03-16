# import socket
# import time


# server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
# # server.bind(("::1", 50000))
# server.bind(("fd04:2240::1cef", 50000))
# server.listen()

# (conn, address) = server.accept()

# while True:
#     time.sleep(1)


import signal
import socket
import socketserver
import struct


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    server.shutdown()


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
        # pieces = [b'']
        # total = 0
        # while b'\n' not in pieces[-1] and total < 10_000:
        #     pieces.append(self.request.recv(2000))
        #     total += len(pieces[-1])
        # self.data = b''.join(pieces)


        print(f"Received from {self.client_address[0]}:")
        
        try:
            while True:
                received_bytes = self.request.recv(2000)

                if not received_bytes:
                    print(f"Connection from {self.client_address} closed.")
                    break

                integer_value = struct.unpack('!I', received_bytes)[0]
                print(integer_value)

        except ConnectionResetError:
            print(f"Connection reset by {self.client_address}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.request.close()  # Ensure socket is closed



        # print(self.data.decode("utf-8"))
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
        # after we return, the socket will be closed.


# signal.signal(signal.SIGINT, signal_handler)

# HOST, PORT = "fd04:2240::1cef", 50000
HOST, PORT = "::", 50000

server = TCPServer6((HOST, PORT), MyTCPHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
