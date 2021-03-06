from pwn import *
from termcolor import colored


class Target:
    def __init__(self, connection, is_remote: bool, process_path):
        self.connection = connection
        self.is_remote = is_remote
        self.process_path = process_path
        if not is_remote:
            binary = process_path.split(" ")[0]
            context.binary = binary
            self.security = ELF(binary).checksec().split("\n")

    def print_security(self):
        print("\nSecurity Mechanisms:")
        for mechanism in self.security:
            if "no" in mechanism.lower():
                split = mechanism.split(":")
                print(f'{split[0]}:{colored(split[1], "red", attrs=["bold"])}')
            else:
                split = mechanism.rsplit(":")
                print(f'{split[0]}:{colored(split[1], "green", attrs=["bold"])}')

    def receive_data(self, timeout=1):
        _data = ""
        while True:
            try:
                response = self.connection.recv(1024, timeout).decode()
            except EOFError:
                break
            if len(response) < 1:
                break
            _data += response
        return _data

    def send_data(self, _data: str):
        self.connection.sendline(_data.encode())

    def is_alive(self):
        return self.connection.poll() is None

    def get_pid(self):
        return self.connection.__getattr__("pid")

    def get_bit_arch(self):
        if not self.is_remote:
            return context.bits
        return -1
