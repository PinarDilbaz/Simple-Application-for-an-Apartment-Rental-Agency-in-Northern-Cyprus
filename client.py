import socket
import sys

class Client:
    def __init__(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        self.server_address = ('127.0.0.1', 10000)

    def start_connection(self):
        try:
            print('connecting to port' + self.server_address[0])
            self.sock.connect(self.server_address)
            response = self.sock.recv(1024)
            print(response)
        except Exception as e:
            print (e)

    def stop_connection(self):
        print('closing socket')
        self.sock.close()

    def send_message(self,message):
        self.sock.sendall(bytes(message, 'utf-8'))
        response = self.sock.recv(1024)
        
        return response
