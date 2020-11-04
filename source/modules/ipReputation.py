#!/usr/bin/env python
import configparser
import sys
#import urllib2
import urllib.request

class IpReputation():
    def __init__(self, target, cnf):
        # Read configuration
        self.config = configparser.RawConfigParser()
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
#                proxy_support = urllib2.ProxyHandler({"http" : \
#                "http://%(proxyuser)s:%(proxypass)s@%(proxyhost)s:%(proxyport)d" % proxyinfo})
                proxy_support = urllib.request.ProxyHandler({"http" : \
                "http://%(proxyuser)s:%(proxypass)s@%(proxyhost)s:%(proxyport)d" % proxyinfo})
#                opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
                opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler)
                # install it
                urllib.request.install_opener(opener)
#                urllib2.install_opener(opener)
            except Exception as err:
                print("***ERROR in proxy initialization: %s" % err)
                print("Check your proxy settings in config.cfg")
                sys.exit()

#        iplist = urllib2.urlopen('http://malc0de.com/bl/IP_Blacklist.txt')
        #iplist = urllib.request.urlopen('http://malc0de.com/bl/IP_Blacklist.txt')  # malc0de block urllib user-agent # netrunn3r
        #req = urllib.request.Request('http://malc0de.com/bl/IP_Blacklist.txt', headers={'User-Agent': 'Mozilla/5.0'})
        #iplist = urllib.request.urlopen(req).read().decode().split('\n')
        with open('data/IP_Blacklist.txt') as iplist:  # create option to choose: online or local file  # netrunn3r
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
    print(IpReputation("192.168.100.48", 'config.cfg').getPayloads())
