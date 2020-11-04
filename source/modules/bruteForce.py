#!/usr/bin/env python
"""
This module tests the ability of the server to track brute force attacks.
This module replaces the old multipleFailedLogins module and is now considered
as a standard module. The old specifics related to multipleFailedLogins have
been withrawn from pytbull.
SF change #3310130 - Thanks to Keith Pawson for the idea ;)
"""

import ConfigParser

class BruteForce():
    def __init__(self, target, cnf):
        # Read configuration
        self.config = ConfigParser.RawConfigParser()
        self.config.read(cnf)

        self._target = target
        self.payloads = []

    def getPayloads(self):

        self.payloads.append([
            "Bruteforce against FTP with ncrack",
            "command",
            [self.config.get('ENV','ncrack'), '-f',
                '-U', self.config.get('ENV','ncrackusers'),
                '-P', self.config.get('ENV','ncrackpasswords'),
                self._target+":21"],
            "(?i)brute"
        ])

        return self.payloads

if __name__ == "__main__":
    print BruteForce('192.168.1.16', 'config.cfg').getPayloads()