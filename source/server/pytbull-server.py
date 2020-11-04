#!/usr/bin/env python
"""
Pytbull server script (reverse shell)
Used for client side attacks

Pytbull is an IDS/IPS testing framework for Snort & Suricata and any IDS/IPS
provided you can grab the alerts file via FTP.
It is developed by Sebastien Damaye (sebastien #dot# damaye #at# gmail #dot# com).
It is shipped with 300 tests grouped in 9 testing modules. For more information,
please refer to <http://www.aldeid.com/index.php/Pytbull>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from optparse import OptionParser
import sys
import socket
import subprocess
import os

class PytbullServer():
    def __init__(self, banner, port):
        # Variable initialization
        self.host = ''
        self.port = port
        self.socksize = 1024

        print banner
        print ""

        # Checking root privs
        print "Checking root privileges".ljust(65, '.'),
        if(os.getuid() != 0):
            print "[ Failed ]"
            print "\n***Error: Root privileges required!"
            sys.exit(0)
        print "[   OK   ]"

    def reverseShell(self):
        print "Checking port to use".ljust(65, '.'),
        try:
            # Open a socket on localhost, port 12345/tcp by default
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.host, int(self.port)))
            print "[   OK   ]"
        except Exception, err:
            print "[ Failed ]"
            print "\n***ERROR: %s" % err
            sys.exit(0)

        print ""
        print "Server started on port: %s" % self.port
        s.listen(1)
        print "Listening..."
        conn, addr = s.accept()
        while True:
            print 'New connection from %s:%d' % (addr[0], addr[1])
            data = conn.recv(self.socksize)
            cmd = ['/bin/sh', '-c', data]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE).wait()
            # Issue 3450032 - Synchronisation issue. The server has to instruct
            # the client that the file has been successfully downloaded before
            # it goes to next file
            conn.send('done')
            if not data:
                break
            elif data == 'killsrv':
                sys.exit()

if __name__ == '__main__':

    banner = """
                                 _   _           _ _
                     _ __  _   _| |_| |__  _   _| | |
                    | '_ \| | | | __| '_ \| | | | | |
                    | |_) | |_| | |_| |_) | |_| | | |
                    | .__/ \__, |\__|_.__/ \__,_|_|_|
                    |_|    |___/
                       Sebastien Damaye, aldeid.com"""
    parser = OptionParser(usage="sudo ./%prog [-p port]")
    parser.add_option("-p", "--port", dest="port", default=12345,
        help="tcp port to open for reverse shell (default to 12345)")

    (options, args) = parser.parse_args(sys.argv)

    # Instantiate Pytbull class
    oPytbullServer = PytbullServer(banner, options.port)
    # Start pytbull reverse shell
    oPytbullServer.reverseShell()
    # Destruct object
    del oPytbullServer
