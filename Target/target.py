from pwn import *


class Target:
    def __init__(self, connection, remote: bool, process):
        self.connection = connection
        self.remote = remote
        self.process = process

    def receive_data(self):
        data = ""
        while True:
            try:
                response = self.connection.recv(1024, 1).decode()
            except EOFError:
                break
            if len(response) < 1:
                break
            data += response
        return data

    def send_data(self, data: str):
        self.connection.sendline(data.encode())

    def is_alive(self):
        return True if self.connection.poll() is None else False
