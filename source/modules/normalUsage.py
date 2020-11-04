#!/usr/bin/env python
###
#
# Written for Simulation of Attacks and Defense by Robert Pallas
#

import ConfigParser

class NormalUsage():
    def __init__(self, target, cnf):
        # Read configuration
        self.config = ConfigParser.RawConfigParser()
        self.config.read(cnf)

        self._target = target
        self.payloads = []

    def getPayloads(self):

	### AB Normal Usage
        self.payloads.append([
            "ApacheBench 10 requests",
            "command",
            "%ab% -k -c 10 -n 10 http://%target%/",
	    ""
            ])

	### ping
        self.payloads.append([
            "Standard ping",
            "command",
            "%ping% -c 1 %target%",
	    ""
            ])

	# POST sthng pcap

        return self.payloads

if __name__ == "__main__":
    print DenialOfService("192.168.100.48").getPayloads()
