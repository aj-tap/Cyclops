#! /usr/bin/env python3

"""
Cyclops: Recon Scripts
usage main.py -t 192.168.112.1/24
"""

from scripts import Enumeration
from scripts import Banner
from scripts import Discovery
import argparse

module_name = "Cyclops: Recon Scripts"
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
    msg = "Cyclops Recon Scripts"
    parser = argparse.ArgumentParser(description=msg)
    parser.add_argument("--host", type=str, required=False, help="Set target Domain/host")
    parser.add_argument('-p', '--ports', help='Specify ports to scan', required=False)
    parser.add_argument('-s', '--scan', help='Scan type (pingscan, crawlPage, dns, portscan ))', required=True)
    parser.add_argument('-v', '--verbose', help='verbose option', required=False, action='store_true')
    args = vars(parser.parse_args())

    invoker.add_command(Banner.WelcomeMessage())
    if args['scan'] == 'crawlPage':
        invoker.add_command(Discovery.DefaultPages(args['host']))
    elif args['scan'] == 'pingscan':
        invoker.add_command(Enumeration.HostDiscovery(args['host']))
    elif args['scan'] == 'portscan':
        invoker.add_command(Enumeration.PortScanner(args['host']))
    elif args['scan'] == 'dns':
        invoker.add_command(Enumeration.DnsResolver(args['host']))
        invoker.add_command(Enumeration.Whois(args['host']))

    invoker.run()