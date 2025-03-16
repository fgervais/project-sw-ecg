import socket
import socketserver
import struct

from threading import Thread


class TCPServer6(socketserver.TCPServer):
    address_family = socket.AF_INET6


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
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


class MyServer(Thread):
    def __init__(self, host="::", port=50000):
        super().__init__()

        self.server = TCPServer6((host, port), MyTCPHandler)

        # self.asked_to_teardown = False

    def teardown(self):
        print("teardown")
        self.server.shutdown()
        self.server.server_close()

        # self.asked_to_teardown = True

    def run(self):
        self.server.serve_forever()
