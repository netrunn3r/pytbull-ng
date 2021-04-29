#!/usr/bin/env python
"""
Pytbull-ng server script (reverse shell)
Used for client side attacks and as a receiver of all attacks

Pytbull-ng is an IDS/IPS testing framework for any IDS/IPS.
Original version, pytbull, was developed by Sebastien Damaye (sebastien #dot# 
damaye #at# gmail #dot# com). Michal Chrobak continue development of this tool
as pytbull-ng, making it more adapted to the current days.

It is shipped with 300 tests grouped in 9 testing modules. For more information,
please refer to <http://www.github.com/netrunn3r/pytbull-ng>.

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
import json

class PytbullServer():
    def __init__(self, banner, port):
        # Variable initialization
        self.host = ''
        self.port = port
        self.socksize = 1024
        self.socket_timeout = 30

        print(banner)
        print("")

        # Checking root privs
        print("Checking root privileges".ljust(65, '.'), end='')
        if(os.getuid() != 0):
            print("[ Failed ]")
            print("\n***Error: Root privileges required!")
            sys.exit(0)
        print("[   OK   ]")

    def reverseShell(self):
        print("Checking port to use".ljust(65, '.'), end='')
        try:
            # Open a socket on localhost, port 12345/tcp by default
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.host, int(self.port)))
            print("[   OK   ]")
        except Exception as err:
            print("[ Failed ]")
            print("\n***ERROR: %s" % err)
            sys.exit(0)

        print("")
        print("Server started on port: %s" % self.port)
        s.listen(1)
        print("Listening...")
        while True:
            try:
                conn, addr = s.accept()
                conn.settimeout(self.socket_timeout)
                data_raw = conn.recv(self.socksize).decode()
                if not data_raw:
                    continue
                print('\n> Orders from %s:%d' % (addr[0], addr[1]))
                data = json.loads(data_raw)
                timeout = data.get("timeout")
                payload = data.get("payload")
                # if payload == 'killsrv':  # unused?
                #     sys.exit()
                print(f'> Command to execute (limit: {timeout}s/{self.socket_timeout}s): {payload}')
                cmd = ['/bin/sh', '-c', payload]
                try:
                    subprocess.run(cmd, timeout=timeout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except subprocess.TimeoutExpired:
                    print("Process timeout...", end='')
                # Issue 3450032 - Synchronisation issue. The server has to instruct
                # the client that the file has been successfully downloaded before
                # it goes to next file
                conn.send('done'.encode())
                conn.close()
            except ConnectionResetError as e:
                print('Connection reset by peer, starting new listener')
            except socket.timeout:
                print('Socket timeout...')

if __name__ == '__main__':

    banner = """
                           __  __          ____                 
              ____  __  __/ /_/ /_  __  __/ / /     ____  ____ _
             / __ \/ / / / __/ __ \/ / / / / /_____/ __ \/ __ `/
            / /_/ / /_/ / /_/ /_/ / /_/ / / /_____/ / / / /_/ / 
           / .___/\__, /\__/_.___/\__,_/_/_/     /_/ /_/\__, /  
          /_/    /____/                                /____/   
           creator of pytbull:    Sebastien Damaye, aldeid.com
           creator of pytbull-ng: Michal Chrobak,   efigo.pl"""
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
