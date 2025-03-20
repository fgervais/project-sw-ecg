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
                received_bytes = self.request.recv(1000)

                if not received_bytes:
                    print(f"Connection from {self.client_address} closed.")
                    break

                integer_value = struct.unpack('!I', received_bytes)[0]
                print(integer_value)
                self.server.dashboard.update_battery_voltage_view(integer_value/1000)

        except ConnectionResetError:
            print(f"Connection reset by {self.client_address}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.request.close()  # Ensure socket is closed


class MyServer(TCPServer6, Thread):
    def __init__(self, dashboard, host="::", port=50000):
        TCPServer6.__init__(self, (host, port), MyTCPHandler)
        Thread.__init__(self)

        self.dashboard = dashboard

        # self.asked_to_teardown = False

    def teardown(self):
        print("teardown")
        self.shutdown()
        self.server_close()

        # self.asked_to_teardown = True

    def run(self):
        self.serve_forever()
