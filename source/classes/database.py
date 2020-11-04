#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sqlite3
import ConfigParser

class DB():
    def __init__(self, cnf):
        # Read configuration
        self.config = ConfigParser.RawConfigParser()
        self.config.read(cnf)
        self._db = self.config.get('PATHS', 'db')

    def addTestResult(self, val):
        """
        Add new entry in table
        """
        conn = sqlite3.connect(self._db)
        conn.text_factory = str
        c = conn.cursor()
        c.execute('insert into test (test_module, test_type, test_dt_start,'
            'test_dt_end, test_name, test_port, test_proto, test_payload,'
            'test_sig_match, test_alert, test_flag)'
            'values (?,?,?,?,?,?,?,?,?,?,?)', val)
        conn.commit()
        c.close()

    def listTests(self, description=None, module=None, port=None, proto=None, payload_fmt=None, test_result=None, payload=None, alert=None):
        """
        List tests
        """
        conn = sqlite3.connect(self._db)
        conn.text_factory = str
        c = conn.cursor()
        nextkeyword = " where "
        filter = ""
        if description!= None and description != '':
            filter += nextkeyword + "test_name like '%%%s%%' ESCAPE '\\'" % description.replace('%', '\%')
            nextkeyword = " and "
        if module!= None and module != 'any':
            filter += nextkeyword + "test_module='%s'" % module
            nextkeyword = " and "
        if port!= None and port != '':
            filter += nextkeyword + "test_port=%s" % port
            nextkeyword = " and "
        if proto != None and proto != 'any':
            filter += nextkeyword + "test_proto='%s'" % proto
            nextkeyword = " and "
        if payload_fmt != None and payload_fmt != 'any':
            filter += nextkeyword + "test_type='%s'" % payload_fmt
            nextkeyword = " and "
        if test_result != None and test_result != 'any':
            filter += nextkeyword + "test_flag=%s" % test_result
            nextkeyword = " and "
        if payload != None and payload != '':
            filter += nextkeyword + "test_payload like '%%%s%%' ESCAPE '\\'" % payload.replace('%', '\%')
            nextkeyword = " and "
        if alert != None and alert != '':
            filter += nextkeyword + "test_alert like '%%%s%%' ESCAPE '\\'" % alert.replace('%', '\%')
        # print """***DEBUG: select * from test %s""" % filter
        c.execute("""select * from test %s""" % filter)
        l = []
        for row in c:
            l.append(row)
        c.close()
        return l

    def truncateTestResults(self):
        """
        Truncate table test
        """
        conn = sqlite3.connect(self._db)
        c = conn.cursor()
        c.execute('delete from test;')
        c.execute('vacuum;')
        conn.commit()
        c.close()

    def getStatsTestsResults(self):
        """
        Get statistics:
        * Total number of tests
        * Number of tests with sig match
        * Number of tests with green (2)
        * Number of tests with orange (1)
        * Number of tests with red (0)
        """
        stats = []
        conn = sqlite3.connect(self._db)
        c = conn.cursor()
        # Total number of tests
        c.execute('select count(*) from test')
        stats.append(c.fetchall()[0][0])
        # Number of tests with sig match
        c.execute('select count(*) from test where test_sig_match is not null')
        stats.append(c.fetchall()[0][0])
        # Number of tests with sig match green (2)
        c.execute('select count(*) from test where test_flag=2')
        stats.append(c.fetchall()[0][0])
        # Number of tests with sig match orange (1)
        c.execute('select count(*) from test where test_flag=1')
        stats.append(c.fetchall()[0][0])
        # Number of tests with sig match red (0)
        c.execute('select count(*) from test where test_flag=0')
        stats.append(c.fetchall()[0][0])

        c.close()
        return stats

    def getStatsModulesDistribution(self):
        stats = []
        conn = sqlite3.connect(self._db)
        c = conn.cursor()
        # Number of tests with sig match red (0)
        c.execute('select distinct(test_module), count(test_module) from test group by test_module')
        for row in c:
            stats.append(row)
        c.close()
        return stats

    def getPayloadFormats(self):
        fmt = []
        conn = sqlite3.connect(self._db)
        c = conn.cursor()
        # Number of tests with sig match red (0)
        c.execute('select distinct(test_type) from test group by test_type')
        for row in c:
            fmt.append(row)
        c.close()
        return fmt

    def getTestDistribModule(self, module):
        """Returns nb of ok, ko, partial for a given module"""
        modules = []
        conn = sqlite3.connect(self._db)
        c = conn.cursor()
        # Number of tests with sig match red (0)
        c.execute('select test_flag, count(test_flag) from test where test_module=? and test_flag is not null group by test_flag order by test_flag desc', (module,))
        for row in c:
            modules.append([row[0], row[1]])
        c.close()

        # Completing missing values...
        r = []
        (c,v) = (0,0)
        for row in modules:
            if row[0]==2:
                c += 1
                v = row[1]
        r.append([2,v])

        (c,v) = (0,0)
        for row in modules:
            if row[0]==1:
                c += 1
                v = row[1]
        r.append([1,v])

        (c,v) = (0,0)
        for row in modules:
            if row[0]==0:
                c += 1
                v = row[1]
        r.append([0,v])

        return r


if __name__ == "__main__":
    print "Truncating table test"
    DB().truncateTestResults()
    print "Initial list"
    DB().listTests()
    print "Adding entry..."
    DB().addTestResult(('test_module', 'test_type', 'test_dt_start', 'test_dt_end', 'test_name',
        80, 'tcp', 'payload', 'test_sig_match', 'test_alerts', 2))
    print "New list"
    DB().listTests()
    