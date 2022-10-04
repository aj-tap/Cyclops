#! /usr/bin/env python3

"""
Cyclops: Recon Automation Scripts
"""

from scripts import Enumeration
from scripts import Banner

module_name = "Cyclops: Recon Automation Scripts"
__version__ = "0.0.1"


class CyclopsInvoker(object):
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def run(self):
        for command in self.commands:
            command.execute()


if __name__ == "__main__":
    invoker = CyclopsInvoker()
    # portScan = PortScanner.PortScanner("127.0.0.1")
    # invoker.add_command({"function": PortScanner, "params": "127.0.0.1"})
    invoker.add_command(Banner.WelcomeMessage())
    invoker.add_command(Enumeration.DnsResolver("google.com"))
    invoker.add_command(Enumeration.PortScanner("127.0.0.1"))
    invoker.run()
