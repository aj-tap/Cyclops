#! /usr/bin/env python3

"""
Cyclops: Recon Automation Scripts
usage main.py -d http://wikipedia.org/
"""

from scripts import Enumeration
from scripts import Banner
from scripts import Discovery
import argparse

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
    msg = "Cyclops Recon Automation Scripts"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("-d", "--domain", type=str, required=True, help="Set target Domain")
    args = parser.parse_args()

    invoker.add_command(Banner.WelcomeMessage())
    # invoker.add_command(Enumeration.DnsResolver("google.com"))
    # invoker.add_command(Enumeration.DnsResolver("facebook.com"))
    # invoker.add_command(Enumeration.Whois("google.com"))
    # invoker.add_command(Enumeration.PortScanner("127.0.0.1"))
    # invoker.add_command(Discovery.DefaultPages("https://en.wikipedia.org/"))
    invoker.add_command(Discovery.DefaultPages(args.domain))
    # invoker.add_command(Discovery.DefaultPages("https://pythonscraping.com/"))
    invoker.run()
