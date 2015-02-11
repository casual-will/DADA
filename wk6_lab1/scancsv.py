from CSVPacket import Packet, CSVPackets
import sys
import argparse

def print_sort_dict(dict):
    for key, value in sorted(dict.iteritems(), key=lambda (k,v): (v,k)):
        print "%s\t:\t%s" % (key, value)

parser = argparse.ArgumentParser()
parser.add_argument("csvfile")
parser.add_argument("-stats", action="store_true")
parser.add_argument("-countip", action="store_true")
args = parser.parse_args()

IPProtos = [0 for x in range(256)]
Ports = [0 for x in range(1024)]
IP = {}
numBytes = 0
numPackets = 0

csvfile = open(args.csvfile,'r')

for pkt in CSVPackets(csvfile):
    # pkt.__str__ is defined...
    #print pkt
    if pkt.tcpdport and pkt.tcpdport < 1024:
        Ports[pkt.tcpdport] += 1
    if pkt.udpdport and pkt.udpdport < 1024:
        Ports[pkt.udpdport] += 1
    if pkt.ipdst:
        if IP.has_key(pkt.ipdst):
            IP[pkt.ipdst] += 1
        else:
            IP[pkt.ipdst] = 1
    if pkt.ipsrc:
        if IP.has_key(pkt.ipsrc):
            IP[pkt.ipsrc] += 1
        else:
            IP[pkt.ipsrc] = 1
    numBytes += pkt.length
    numPackets += 1
    proto = pkt.proto & 0xff
    IPProtos[proto] += 1

#print "numPackets:%u numBytes:%u" % (numPackets,numBytes)
#for i in range(256):
#    if IPProtos[i] != 0:
#        print "%3u: %9u" % (i, IPProtos[i])
if args.stats:
    for i in range(1024):
        if Ports[i] != 0:
            print "%3u: %9u" % (i, Ports[i])

if args.countip:
    print_sort_dict(IP)

