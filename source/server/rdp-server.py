#!/usr/bin/env python
"""
Pytbull-ng server script (rdp server)
Used for bruteforce to rdp service

Client only send username, then rdp server response with negotiation failure.
TODO: Make full RDP authentication to better mimmic real RDP traffic
"""
import socket
import re
import datetime
import os
import sys
import logging
from optparse import OptionParser

class RDPServer():
    def __init__(self, port, debug):
            # Variable initialization
            self.host = ''
            self.port = port
            self.socksize = 4096
            self.socket_timeout = 30
            logging.basicConfig(level=debug)

            # Checking root privs
            logging.debug("Checking root privileges".ljust(65, '.'))#, end='')
            if(os.getuid() != 0):
                logging.debug("[ Failed ]")
                logging.debug("\n***Error: Root privileges required!")
                sys.exit(0)
            logging.debug("[   OK   ]")

    def extract_username(self, data):
        """Extract username via regex or return None"""
        match = re.search(r'mstshash=(?P<username>[a-zA-Z0-9-_@]+)', data)
        if match:
            uname = match.group('username')
            return uname
        return None

    def run(self):
        logging.debug("Checking port to use".ljust(65, '.'))#, end='')
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.host, int(self.port)))
            logging.debug("[   OK   ]")
        except Exception as err:
            logging.debug("[ Failed ]")
            logging.debug(f"\n***ERROR: {err}")
            sys.exit(0)
        s.listen(1)

        while True:
            try:
                logging.debug("Starting socket accept...")
                conn, addr = s.accept()
                conn.settimeout(self.socket_timeout)
                address = addr[0].strip()
                logging.debug(f"Connection from: {address}")
                data = conn.recv(self.socksize).decode('cp437')  # cp437 because we have non-English symbols
                st = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                user = self.extract_username(data)
                logging.debug(f"Received data from {address} with user {user} at {st}")
                logging.debug("Sending RDP_NEG_FAILURE")
                conn.send(b"0x00000004 RDP_NEG_FAILURE")
                conn.close()
                logging.debug("Shutdown connection and closed...")
            except Exception as e:
                logging.debug(f"EXCEPTION: {repr(e)}")
                conn.close()

if __name__ == '__main__':
    parser = OptionParser(usage="sudo ./%prog [-p port]")
    parser.add_option("-p", "--port", dest="port", default=3389,
        help="tcp port to open for fake rdp server (default to 3389)")
    parser.add_option("-d", "--debug", dest="debug_flag", default=False,
        help="print debug information (default false)")

    (options, args) = parser.parse_args(sys.argv)

    if options.debug_flag:
        debug = logging.DEBUG
    else:
        debug = logging.INFO

    oRDPServer = RDPServer(options.port, debug)
    oRDPServer.run()
    del oRDPServer                