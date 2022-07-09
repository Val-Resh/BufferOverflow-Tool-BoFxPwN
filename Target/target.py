from pwn import *

class Target:

    def __init__(self, connection, remote: bool):
        self.connection = connection
        self.remote = remote

    def receive_data(self):
        data = ""
        while True:
            response = self.connection.recv(1024, 10).decode()
            if len(response) < 1:
                break
            data += response
        return data
