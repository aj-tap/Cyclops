import sys
import socket
import pyfiglet


# commands
class PortScanner:
    def __init__(self, ip_addr, ports=None, timeout=0.5):
        if ports is None:
            ports = [*range(1, 65535)]
        self.ip_addr = ip_addr
        self.ports = ports
        self.open_ports = []
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
                # print(f"port {port} is open")
            # else:
            # print(f"port {port} is closed")


#portscanner = PortScanner("127.0.0.1")
#portscanner.run()
#print(portscanner.getOpenPorts())
