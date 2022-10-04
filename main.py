#! /usr/bin/env python3

"""
Cyclops:
"""

import pyfiglet
from modules import PortScanner

ascii_banner1 = pyfiglet.figlet_format("Cyclops \n", 'slant')
ascii_banner2 = pyfiglet.figlet_format("made by \n aj-tap & axojolotl", "digital")


module_name = "Cyclops: Recon Automation Scripts"
__version__ = "0.0.1"


class Cyclops:
    def __init__(self, receiver, text):
        self.receiver = receiver
        self.text = text

    def execute(self):
        self.receiver.print_message(self.text)


