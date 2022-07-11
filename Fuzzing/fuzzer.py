import string

from Target.target import Target
from Target.target_factory import create_target
from pwn import *


class Fuzzer:
    registers_arch = {"64": ["rip", "rsp"],
                      "32": ["eip", "esp"]}

    def indentify_crash(self, target: Target, attempts: int = 100):
        _size = 100
        for i in range(attempts):
            payload = 'A' * _size
            try:
                target.receive_data()
                target.send_data(payload)
                response = target.receive_data()
                if len(response) < 1:
                    return _size
                _size += 100
            except Exception:
                target.connection.kill()
            if not target.is_alive():
                target = create_target(target.process)
        return 0

    def get_offset(self, target: Target, _size: int):
        pattern_style = string.ascii_uppercase
        if target.is_remote:
            return -1
        pattern = cyclic(length=_size, alphabet=pattern_style)
        gdb_execute = f'/usr/bin/gdb -pid={target.get_pid()}'
        debugger = create_target(gdb_execute)

        for i in range(3):
            if i == 1:
                debugger.send_data("\n")
            debugger.receive_data()

        target.receive_data()
        debugger.send_data("set style enabled off")
        debugger.receive_data()
        debugger.send_data("continue")
        debugger.receive_data()
        target.send_data(pattern)
        debugger.receive_data()

        for register in self.registers_arch[str(target.get_bit_arch())]:
            debugger.send_data(f"x ${register}")
            memory = debugger.receive_data().replace("\t", " ").replace("\n", " ").split(" ")
            pointer_register = memory[1] if "sp" in register  \
                else memory[0]

            print(pointer_register)

            if pointer_register[len(pointer_register)-1] == ":":
                pointer_register = pointer_register[:-1]

            if len(pointer_register) > 10:
                pointer_register = pointer_register[2:]
                while len(pointer_register) > 8:
                    pointer_register = pointer_register[1:]
                pointer_register = f'0x{pointer_register}'

            offset = cyclic_find(int(pointer_register, 16), alphabet=pattern_style)
            if offset > 0:
                debugger.connection.kill()
                return offset

        debugger.connection.kill()
        return -1
