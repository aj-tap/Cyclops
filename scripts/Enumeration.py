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


class HostDiscovery:
    def __init__(self, targetHost):
        self.targetHost = str(targetHost)
        self.portRange = "0"
        self.Ether = scapy.Ether()
        self.ARP = scapy.ARP()
        self.ICMP = scapy.ICMP()
        self.IP = scapy.IP()
        self.TCP = scapy.TCP()
        self.UDP = scapy.UDP()

    def performArpPing(self, broadcastDestination="ff:ff:ff:ff:ff:ff", timeout=0):
        self.Ether.dst = broadcastDestination
        self.ARP.pdst = self.targetHost
        request_broadcast = self.Ether / self.ARP
        clients = scapy.srp(request_broadcast, timeout=1)[0]
        self.printMsg("Performing Arp Ping")
        for element in clients:
            print(element[1].psrc + "      " + element[1].hwsrc)
        print(str(len(clients)) + " Alive Host")

    def performIcmpPing(self, ttl=20):
        self.IP.dst = self.targetHost
        self.IP.ttl = ttl
        request_ICMP_ping = self.IP / self.ICMP
        self.printMsg("Performing ICMP Ping")
        ans, unans = scapy.sr(request_ICMP_ping)
        print(ans.summary())

    def performTcpSynPing(self, port=80):
        self.IP.dst = self.targetHost
        self.TCP.dport = port
        self.TCP.flags = "S"
        request_TCP_ping = self.IP / self.TCP

        # ans, unans = sr(IP(dst=host)/TCP(dport=port, flags="S"))
        self.printMsg("Performing TCP Ping")
        ans, unans = scapy.sr(request_TCP_ping)
        print(ans.summary())

    def performTcpAckScan(self):
        self.IP.dst = self.targetHost
        self.TCP.flags = "A"
        self.TCP.dport = 80
        request_ACK_Scan = self.IP / self.TCP
        ans, unans = scapy.sr(request_ACK_Scan)
        print(ans.summary())

    def performUdpPing(self):
        self.IP.dst = self.targetHost
        request_UDP_ping = self.IP / self.UDP
        self.printMsg("Performing UDP Ping")
        ans, unans = scapy.sr(request_UDP_ping)
        print(ans.summary())

    def performIPscan(self):
        self.IP.dst = self.targetHost
        self.IP.proto = (0, 255)
        self.printMsg("Performing IP scan")
        requestIpScan = self.IP / "Hello"
        ans, unans = scapy.sr(requestIpScan, retry=2)
        print(ans.summary())

    def printMsg(self, msg):
        print("\n" + "****" * 20)
        print(msg)
        print("****" * 20)

    def execute(self):
        # self.performTCPAckScan()
        # self.performIPscan()
        self.performIcmpPing()
        self.performArpPing()
        self.performTcpSynPing()
        self.performTcpAckScan()
        self.performUdpPing()
