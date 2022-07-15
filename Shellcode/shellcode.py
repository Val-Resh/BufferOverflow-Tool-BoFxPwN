from Target.target import Target


class Shellcode:
    def __init__(self, target: Target):
        self.target = target
        self.bad_characters = "\x00"
        self.shellcode = ""

    def identify_bad_chars(self):
        pass

    def get_hex_chars(self):
        hex_chars = str()
        for i in range(1, 256):
            hex16 = hex(i).split("x")[1]
            if len(hex16) < 2:
                hex16 = f'0{hex16}'
            hex_chars += f"\\x{hex16}"
        return hex_chars

