#!/usr/bin/env python
###
# @author $Author: sebastiendamaye $
# @version $Revision: 12 $
# @lastmodified $Date: 2011-05-26 21:25:30 +0200 (Thu, 26 May 2011) $
#

import ConfigParser

class TestRules():
    def __init__(self, target, cnf):
        # Read configuration
        self.config = ConfigParser.RawConfigParser()
        self.config.read(cnf)

        self._target = target
        self.payloads = []

    def getPayloads(self):
        ### Simple LFI
        self.payloads.append([
            "Simple LFI",
            "socket",
            80,
            "tcp",
            "GET /index.php?page=../../../etc/passwd HTTP/1.1\r\nHost: %localhost%\r\nUser-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041202 Firefox/1.0\r\n\r\n",
            "1:1122:8"
            ])

        ### LFI using NULL byte
        self.payloads.append([
            "LFI using NULL byte",
            "socket",
            80,
            "tcp",
            "GET /index.php?page=../../../etc/passwd%00 HTTP/1.1\r\nHost: 127.0.0.1\r\nUser-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041202 Firefox/1.0\r\n\r\n",
            "1:1122:8"
            ])

        ### Full SYN Scan
        self.payloads.append([
            "Full SYN Scan",
            "command",
            "%sudo% %nmap% -sS -p- %target%",
            "122:1:1"
            ])

        ### Full Connect() Scan
        self.payloads.append([
            "Full Connect() Scan",
            "command",
            [self.config.get('ENV','nmap'), '-sT', '-p-', self._target],
            "122:1:1"
            ])

        ### SQL Injection
        self.payloads.append([
            "SQL Injection",
            "socket",
            80,
            "tcp",
            "GET /form.php?q=1+UNION+SELECT+VERSION%28%29 HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n",
            "(?i)UNION"
            ])

        ### Netcat Reverse Shell
        self.payloads.append([
            "Netcat Reverse Shell",
            "socket",
            22,
            "tcp",
            "/bin/sh",
            "1:1324:10"
            ])

        ### Nikto Scan
        # [self.config.get('ENV','sudo'), self.config.get('ENV','nikto'), '-config', self.config.get('ENV','niktoconf'), '-h', self._target, '-Plugins', 'cgi'],
        self.payloads.append([
            "Nikto Scan",
            "command",
            "%sudo% %nikto% -config %niktoconf% -h %target% -Plugins cgi",
            "(?i)nikto"
            ])

        return self.payloads

if __name__ == "__main__":
    print TestRules("192.168.100.48").getPayloads()