import sys
import socket


class PortScanner:
    def __init__(self, ip_addr, ports=None, timeout=0.5):
        if ports is None:
            ports = [*range(1, 65535)]
        self.ip_addr = ip_addr
        self.ports = ports
        self.open_ports = []
        self.closed_ports = []
        self.timeout = timeout

    def probe_port(self, ip_addr, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        try:
            s.connect((ip_addr, port))
            return True
        except:
            return False

    def getOpenPorts(self):
        return self.open_ports

    def getIpAddr(self):
        return self.ip_addr

    def execute(self):
        for port in self.ports:
            sys.stdout.flush()
            if self.probe_port(self.ip_addr, port):
                self.open_ports.append(port)
            else:
                self.closed_ports.append(port)
        print("Open Ports : ", self.getOpenPorts())


class DnsResolver:
    def __init__(self, domain):
        self.ip_addr = None
        self.domain = domain

    def set_domain(self, domain):
        self.domain = domain

    def get_host(self):
        return str(self.domain)

    def execute(self):
        self.ip_addr = socket.gethostbyname(self.domain)
        print("Domain :", self.domain, "is ", self.ip_addr)


class Whois:
    def __init__(self, domain):
        # self.ip_addr = None
        self.domain = domain
        self.whois = 'whois.internic.net'

    def perform_whois(self, server, query):
        msg = ""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, 43))
        s.send(query + '\r\n')

        while len(msg) < 10000:
            chunk = s.recv(100)
            if chunk == '':
                break
            msg = msg + chunk
        return msg

    def get_whois_data(self):
        msg = None
        self.domain = str(self.domain).replace('http://', '')
        self.domain = str(self.domain).replace('www.', '')
        ext = self.domain[-3:]
        if ext == 'com' or ext == 'org' or ext == 'net':
            msg = self.perform_whois(self.whois, self.domain)

        lines = msg.splitlines()
        for line in lines:
            if ':' in line:
                words = line.split(':')
                if 'Whois' in words[0] and 'whois.' in words[1]:
                    whois = words[1].strip()
                    break

    def execute(self):
        print(self.get_whois_data())
