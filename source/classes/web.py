#!/usr/bin/env python
#-*- coding: utf-8 -*-

import cherrypy
import database

class Footer:
    def footer(self):
        footer = """
            <div id="footer">
                <div style="padding:10px;">pytbull is developed and maintained by S&eacute;bastien Damaye</div>
                <div><a href="http://pytbull.sourceforge.net" style="color:#fff;">pytbull.sf.net</a>&nbsp;|&nbsp;<a href="http://www.aldeid.com" style="color:#fff;">aldeid.com</a></div>
            </div>
            </body>
            </html>"""
        return footer

class Main:

    def __init__(self, cnf):
        self.cnf = cnf
        
    def flag2title(self, flag):
        t = ''
        if flag==0:
            t = 'no detection'
        elif flag == 1:
            t = 'partial detection'
        elif flag==2:
            t = 'full detection'
        return t
        
    def index(self):
        index ="""
            <!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
                <title>pytbull report</title>
                <script type="text/javascript" src="/js/jquery.js"></script>
                <script type="text/javascript" src="/js/jquery.jqplot.js"></script>
                <script type="text/javascript" src="/js/plugins/jqplot.pieRenderer.js"></script>
                <script type="text/javascript" src="/js/plugins/jqplot.donutRenderer.js"></script>
                <script type="text/javascript" src="/js/plugins/jqplot.dateAxisRenderer.js"></script>
                <script type="text/javascript" src="/js/plugins/jqplot.canvasTextRenderer.js"></script>
                <script type="text/javascript" src="/js/plugins/jqplot.canvasAxisTickRenderer.js"></script>
                <script type="text/javascript" src="/js/plugins/jqplot.categoryAxisRenderer.js"></script>
                <script type="text/javascript" src="/js/plugins/jqplot.barRenderer.js"></script>
                <link rel="stylesheet" type="text/css" href="/js/jquery.jqplot.css" />
                <link rel="stylesheet" type="text/css" href="/styles2.css" />"""
        testresults = database.DB(self.cnf).getStatsTestsResults()
        index += """<script type="text/javascript">
            $(document).ready(function(){
              var data = [
                ['full detection', %d],['partial detection', %d], ['no detection', %d]
              ];
              var plot1 = jQuery.jqplot ('chart1', [data],
                {
                  title: 'Tests results',
                  seriesColors: ["#61C200", "#FF8000", "#ff0000"],
                  seriesDefaults: {
                    renderer: jQuery.jqplot.PieRenderer,
                    rendererOptions: {
                      showDataLabels: true
                    }
                  },
                  legend: { show:true, location: 'e' }
                }
              );
            });
            </script>""" % (testresults[2], testresults[3], testresults[4])
        moddistrib = database.DB(self.cnf).getStatsModulesDistribution()
        s = "["
        for i in moddistrib:
            s += "['%s', %d]," % (i[0], i[1])
        s = s[:-1] + "]"
        index += """<script type="text/javascript">
            $(document).ready(function(){
                var line1 = %s;

                var plot1 = $.jqplot('chart2', [line1], {
                title: 'Modules distribution',
                series:[{renderer:$.jqplot.BarRenderer}],
                axesDefaults: {
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer ,
                    tickOptions: {
                      angle: -30,
                      fontSize: '10pt'
                    }
                },
                axes: {
                  xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer
                  }
                }
                });
            });
            </script>""" % s

        # Donuts for each module
        for i in moddistrib:
            res = database.DB(self.cnf).getTestDistribModule(i[0])
            if sum(r[1] for r in res)!=0:
                index += """<script type="text/javascript">
                    $(document).ready(function(){"""
                index += """var s1 = ["""
                for r in res:
                    index += "['%s',%d]," % (self.flag2title(r[0]), r[1])
                index += "];"
                index += """var plot3 = $.jqplot('%s', [s1], {
                        title: '%s',
                        seriesColors: ["#61C200", "#FF8000", "#ff0000"],
                        seriesDefaults: {
                          // make this a donut chart.
                          renderer:$.jqplot.DonutRenderer,
                          rendererOptions:{
                            // Donut's can be cut into slices like pies.
                            sliceMargin: 3,
                            // Pies and donuts can start at any arbitrary angle.
                            startAngle: -90,
                            showDataLabels: true,
                            // By default, data labels show the percentage of the donut/pie.
                            // You can show the data 'value' or data 'label' instead.
                            dataLabels: 'value'
                          }
                        },
                        legend: {
                          show: true,
                          location: 'e',
                          placement: 'inside'
                        }
                      });
                    });
                    </script>""" % (i[0], i[0])

        index += """</head>
            <body>"""
        index += """<div id="container">
            <div id="header">
                <div><a href="/" title="home"><img src="/img/logo.png" alt="pytbull logo" /></a></div>
                <ul id="menu">
                    <li><a href="/">Stats</a></li>
                    <li><a href="/details">Details</a></li>
                    <li><a href="/search">Search</a></li>
                </ul>
            </div>
            <div style="clear:both"></div>
            <div id="content">"""
        index += """<h1>Global stats</h1>
            <div id="chart1" style="float:left;height:300px;width:400px;"></div>
            <div id="chart2" style="float:left;height:300px;width:400px;"></div>
            <div style="clear:both"></div>"""

        # Donuts
        index += """<h1>Modules stats</h1>"""
        for i in moddistrib:
            res = database.DB(self.cnf).getTestDistribModule(i[0])
            if sum(r[1] for r in res)!=0:
                index += """<div id="%s" style="width:270px;height:200px;float:left"></div>""" % i[0]
        index += """<div style="clear:both;"></div></div>"""
        index += Footer().footer()
        return index
    index.exposed = True

class Details:
    def __init__(self, cnf):
        self.cnf = cnf

    def index(self, description=None, module=None, port=None, proto=None, payload_fmt=None, test_result=None, payload=None, alert=None):
        index ="""
            <!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
                <title>pytbull report</title>
                <link rel="stylesheet" type="text/css" href="/styles2.css" />
                <script type="text/javascript">
                    function expandcollapse(id) {
                        var browser = navigator.appName;
                        if(browser == "Netscape"){
                            var showstr = 'table-row';
                        } else {
                            var showstr = 'block';
                        }
                        document.getElementById(id).style.display = (document.getElementById(id).style.display=='none')?showstr:'none';
                        document.getElementById('img_'+id).src = (document.getElementById(id).style.display=='none')?'/img/expand.png':'/img/collapse.png';
                    }
                </script>
            </head>
            <body>"""
        index += """<div id="container">
            <div id="header">
                <div><a href="/" title="home"><img src="/img/logo.png" alt="pytbull logo" /></a></div>
                <ul id="menu">
                    <li><a href="/">Stats</a></li>
                    <li><a href="/details">Details</a></li>
                    <li><a href="/search">Search</a></li>
                </ul>
            </div>
            <div style="clear:both"></div>
            <div id="content">"""

        ### Filters
        filter = []
        port, proto, payload_fmt, test_result, payload, alert
        if description!=None and description!= '':
            filter.append(["Description", description])
        if module!=None and module!='any':
            filter.append(["Module", module])
        if port!=None and port!='':
            filter.append(["Port", port])
        if proto!=None and proto!='any':
            filter.append(["Proto", proto])
        if payload_fmt!=None and payload_fmt!='any':
            filter.append(["Format", payload_fmt])
        if test_result!=None and test_result!='any':
            if test_result == "0":
                res = "no detection"
            elif test_result=="1":
                res = "partial detection"
            elif test_result=="2":
                res = "full detection"
            filter.append(["Result", res])
        if payload!=None and payload!='':
            filter.append(["Payload", payload])
        if alert!=None and alert!='':
            filter.append(["Alert", alert])
        #display filters
        if len(filter) != 0:
            index += """<div style="padding:5px;">"""
            index += """<div style="float:left;padding:3px;"><strong>Filters: </strong></div>"""
            for f in filter:
                index += """<div style="float:left;padding:2px;margin-left:5px;border:solid 1px #284655; background:#93C4D9;-moz-border-radius:5px;border-radius:5px;">%s=%s</div>""" % (f[0], f[1])
            index += """<div style="clear:both"></div></div>"""

        index += """\n<table border="1" style="width:800px;">
            <tr>
                <th></th>
                <th>#</th>
                <th>Description</th>
                <th>Module</th>
                <th>Port</th>
                <th>Payload fmt</th>
                <th>Result</th>
            </tr>"""
        for test in database.DB(self.cnf).listTests(description, module, port, proto, payload_fmt, test_result, payload, alert):
            index += """\n<tr id="tr_%d">""" % test[0]
            # Expand / collapse
            index += """\n<td><a href="javascript:expandcollapse(%d)"><img id="img_%d" src="/img/expand.png" alt="expand/collapse"/></a></td>""" % (test[0],test[0])
            # id_test
            index += """\n<td>%d</td>""" % test[0]
            # test_name
            index += """\n<td>%s</td>""" % test[5]
            # test_module
            index += """\n<td>%s</td>""" % test[1]
            # port / proto
            if test[6]!=None:
                index += """\n<td>%s/%s</td>""" % (test[6], test[7])
            else:
                index += """\n<td></td>"""
            # Payload format (Test type)
            index += """\n<td>%s</td>""" % test[2]
            # test flag
            if test[9]!=None:
                index += """\n<td><img src="/img/traffic_light_%s.png" alt="traffic light" /></td>""" % test[11]
            else:
                index += """\n<td></td>"""
            index += "\n</tr>"

            index += """\n<tr id="%d" style="display:none;"><td colspan="7" style="border:solid 3px #284655;background:#E9ECF0;">""" % test[0]
            index += "<ul>"
            index += """<li><strong>Start:</strong> %s</li>""" % test[3]
            index += """<li><strong>End:</strong> %s</li>""" % test[4]
            index += """<li><strong>Sig match:</strong> %s</li>""" % test[9]
            index += "</ul>"
            if test[8]!='' and test[8]!=None:
                index += """<div><strong>Payload:</strong></div>"""
                try:
                    index += """<div><textarea style="width:750px;height:70px;">%s</textarea></div>""" % test[8]
                except:
                    index += """<div>***Error: Can not be displayed</div>"""
            index += """<div><strong>Alerts:</strong></div>"""
            index += """<div><textarea style="width:750px;height:200px;">%s</textarea></div>""" % test[10]
            index += """</td></tr>"""

        index += """\n</table>"""
        index += """</div>"""
        index += Footer().footer()
        return index
    index.exposed = True


class Search:
    def __init__(self, cnf):
        self.cnf = cnf
    
    def index(self):
        index ="""
            <!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
                <title>pytbull report</title>
                <link rel="stylesheet" type="text/css" href="/styles2.css" />
            </head>
            <body>"""
        index += """<div id="container">
            <div id="header">
                <div><a href="/" title="home"><img src="/img/logo.png" alt="pytbull logo" /></a></div>
                <ul id="menu">
                    <li><a href="/">Stats</a></li>
                    <li><a href="/details">Details</a></li>
                    <li><a href="/search">Search</a></li>
                </ul>
            </div>
            <div style="clear:both"></div>
            <div id="content">"""
        index += """
            <form action="/details" method="get">
                <table><tr><td style="vertical-align:top;width:350px;">"""
        
        ### Description
        index += """
                <div style="float:left;width:100px;"><strong>Description</strong></div>
                <div style="float:left"><input type="text" name="description" style="width:200px;" /></div>
                <div style="clear:both"></div>"""

        ### Modules
        index += """
                <div style="float:left;width:100px;"><strong>Modules*</strong></div>
                <div style="float:left">
                    <select name="module">
                        <option value="any">any</option>"""
        modules = database.DB(self.cnf).getStatsModulesDistribution()
        for module in modules:
            index += """<option value="%s">%s</option>""" % (module[0], module[0])
        index += """</select>"""
        index += """
                </div>
                <div style="clear:both"></div>"""
                
        ### Port / proto
        index += """
                <div style="float:left;width:100px;"><strong>Port/Proto</strong></div>
                <div style="float:left"><input type="text" name="port" style="width:30px;" /></div>
                <div style="float:left">/</div>
                <div style="float:left">
                    <select name="proto">
                        <option value="any">any</option>
                        <option value="tcp">tcp</option>
                        <option value="udp">udp</option>
                    </select>
                </div>
                <div style="clear:both"></div>"""

        ### Separator
        index += """</td><td style="vertical-align:top;">"""

        ### Payload formats
        index += """
                <div style="float:left;width:100px;"><strong>Payload format</strong></div>
                <div style="float:left">
                    <select name="payload_fmt">
                        <option value="any">any</option>"""
        payload_formats = database.DB(self.cnf).getPayloadFormats()
        for fmt in payload_formats:
            index += """<option value="%s">%s</option>""" % (fmt[0], fmt[0])
        index += """
                    </select>
                </div>
                <div style="clear:both"></div>"""

        ### Test results
        index += """
                <div style="float:left;width:100px;"><strong>Test result</strong></div>
                <div style="float:left">
                    <select name="test_result">
                        <option value="any">any</option>
                        <option value="2">full detection</option>
                        <option value="1">partial detection</option>
                        <option value="0">no detection</option>
                    </select>
                </div>
                <div style="clear:both"></div>"""

        ### Payload
        index += """
                <div style="float:left;width:100px;"><strong>Payload</strong></div>
                <div style="float:left"><input type="text" name="payload" style="width:200px;" /></div>
                <div style="clear:both"></div>"""

        ### Alert
        index += """
                <div style="float:left;width:100px;"><strong>Alert</strong></div>
                <div style="float:left"><input type="text" name="alert" style="width:200px;" /></div>
                <div style="clear:both"></div>"""

        ### End of form
        index += """
                </td></tr>
                <tr><td colspan="2" style="text-align:center;height:50px"><input type="submit" value="Search" /></td>
                </tr></table>
            </form>"""
        index += """</div>"""
        index += Footer().footer()
        return index
    index.exposed = True


if __name__ == "__main__":

    main = Main()
    main.details = web.Details()

    cherrypy.quickstart(main)