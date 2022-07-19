from termcolor import colored


class Console:
    CONSOLE = colored("BoFxPwN", "blue", attrs=["underline"])+colored(" > ", "blue")

    def __str__(self):
        return self.CONSOLE


