import pyfiglet


class WelcomeMessage:
    def __init__(self):
        self.ascii_banner1 = pyfiglet.figlet_format("Cyclops \n", 'slant')
        self.ascii_banner2 = pyfiglet.figlet_format("made by \n aj-tap & axojolotl", "digital")

    def execute(self):
        print(self.ascii_banner1, "\n", self.ascii_banner2)
