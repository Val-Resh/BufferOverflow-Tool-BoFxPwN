from Target.target import Target
from Target.target_factory import create_target
from pwn import *


class Fuzzer:
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

    #TODO INCOMPLETE
    def get_offset(self, target: Target, _size: int):
        if target.is_remote:
            return -1
        pattern = cyclic(length=_size, alphabet=string.ascii_uppercase)
        gdb_execute = f'/usr/bin/gdb -pid={target.get_pid()}'
        debugger = create_target(gdb_execute)

        for i in range(3):
            if i == 1:
                debugger.send_data("\n")
            debugger.receive_data()

        target.receive_data()
        target.send_data(pattern)

        debugger.send_data("info registers\n")
        print(debugger.receive_data())

        # python print(gdb.selected_frame().read_register('rip'))



