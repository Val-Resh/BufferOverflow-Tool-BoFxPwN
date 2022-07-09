"""
Target factory is responsible for creating instances of a Target object.
"""
from Target.target import Target
from pwn import *


def create_target(target: str):
    if ":" in target:
        target = target.split(":")
        try:
            return Target(remote(target[0], int(target[1])), True)
        except PwnlibException:
            print(f'Unable to connect to {target[0]}:{target[1]}, please ensure host is up.\nFormat: IP:PORT')
    else:
        try:
            return Target(process(target.split(" ")), False)
        except PwnlibException:
            print(f'Unable to start local process {target}, please ensure the binary name is correct.\nExample: '
                  f'./my_vuln_binary')