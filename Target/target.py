from pwn import *

class Target:

    def __init__(self, connection):
        self.connection = connection
