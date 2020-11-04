#!/usr/bin/env python
import ConfigParser
import urllib2

class IpReputation():
    def __init__(self, target, cnf):
        # Read configuration
        self.config = ConfigParser.RawConfigParser()
        self.config.read(cnf)

        self._target = target
        self.payloads = []
        self.lowreputation = []

        # Proxy settings / initialization
        if self.config.get('CLIENT','useproxy')=='1':
            proxyinfo = {
                'proxyuser' : self.config.get('CLIENT','proxyuser'),
                'proxypass' : self.config.get('CLIENT','proxypass'),
                'proxyhost' : self.config.get('CLIENT','proxyhost'),
                'proxyport' : int(self.config.get('CLIENT','proxyport'))
            }
            try:
                # build a new opener that uses a proxy requiring authorization
                proxy_support = urllib2.ProxyHandler({"http" : \
                "http://%(proxyuser)s:%(proxypass)s@%(proxyhost)s:%(proxyport)d" % proxyinfo})
                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
                # install it
                urllib2.install_opener(opener)
            except Exception, err:
                print "***ERROR in proxy initialization: %s" % err
                print "Check your proxy settings in config.cfg"
                sys.exit()

        iplist = urllib2.urlopen('http://malc0de.com/bl/IP_Blacklist.txt')
        for ip in iplist:
            if not ip.startswith('\n') and not ip.startswith('//'):
                self.lowreputation.append(ip.split('\n')[0])


    def getPayloads(self):

        for i in range(int(self.config.get('TESTS_PARAMS','ipreputationnbtests'))):
            self.payloads.append([
                "IP Reputation %s" % self.lowreputation[i],
                "scapy",
                """send(IP(src="%s",dst="%s")/TCP(sport=80)/"fake.exe", verbose=0)""" % (self.lowreputation[i], self._target),
                "(?i)rbn"
                ])

        return self.payloads

if __name__ == "__main__":
    print IpReputation("192.168.100.48", 'config.cfg').getPayloads()
