#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Plugin purpose
==============

Fetch teleinfo data from a MySQL db.

Implements
==========

- teleinfo from mysql

@author: kbu <kbu@kbulabs.fr>
@copyright: (C) 2007-2016 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

from domogik.xpl.common.xplmessage import XplMessage
from domogik.xpl.common.plugin import XplPlugin


#import os
#try:
#        user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
#except KeyError:
#        user_paths = []
#print user_paths

#from domogik_packages.plugin_timysql.lib.teleinfo_mysql import TeleinfoMysql
#from test.teleinfo_mysql import teleinfomysql
from domogik_packages.plugin_timysql.lib.teleinfo_mysql import TeleinfoMysql

import threading
import traceback

class TimysqlManager(XplPlugin):
    """ Bin part of the teleinfo_mysql plugin """

    def __init__(self):
        """ The constructor of your class. This function  will be called when the class is instantiated.
        """
        XplPlugin.__init__(self, name='timysql')

        # handle the configuration part

        # check if the plugin is configured. If not, this will stop the plugin and log an error
        #if not self.check_configured():
        #        return
        

        #self.devices = self.get_device_list(quit_if_no_device = True)
        self.devices = self.get_device_list(quit_if_no_device = False)
        #self.log.debug("\n\n")
        #self.log.debug("self.devices : {}".format(self.devices))
        #self.log.debug("\n\n")


        # link to my lib
        timysql_manager = TeleinfoMysql(self.log, self.send_xpl, self.get_stop())
        #timysql_manager.test_callback();

        #put a hard interval
        #interval = 30     
        
        threads = {}
        for dev in self.devices:
            try:
                if not self.check_configured():
                    self.log.error("Device {} is not configured !".format(dev['name']))
                    return
                interval = self.get_parameter(dev, "interval")
                if interval == None:
                    self.log.error("Interval \"{}\" is invalid for device \"{}\"".format(interval, dev['name']))
                    break
                #else:
                #    print "DEBUG : interval = {}".format(interval)

                thr_name = "dev_{}".format(dev['id'])
                self.log.info("[Starting thread {}] Start fetching teleinfo data from mysql for device {}".format(thr_name, dev['name']))
                threads[thr_name] = threading.Thread(None,
                                                    timysql_manager.get_last_teleinfo,
                                                    thr_name,
                                                    (interval,),
                                                    {})
                threads[thr_name].start()
                self.register_thread(threads[thr_name])
            except:
                self.log.error("{0}".format(traceback.format_exc()))
                self.log.error("ERROR : exit plugin timysql")
                return

        self.log.info("Plugin \"timysql\" ready :)")
        self.ready()


    def send_xpl(self, teleinfo):
        """ send xPL on the network """
        self.log.debug("Send xPL msg with a line of teleinfo data")

        #print "callback : receive frame is : \n\n"
        #print teleinfo
        #print "\n\n"

        # creation du message xPL
        msg = XplMessage()
        msg.set_type("xpl-stat")
        #msg.set_schema("sensor.basic")
        msg.set_schema("teleinfo.basic")
        #msg.add_data({"timestamp" : teleinfo["timestamp"]})
        #msg.add_data({"recdate" : teleinfo["recdate"]})
        #msg.add_data({"rectime" : teleinfo["rectime"]})
        msg.add_data({"optarif" : teleinfo["optarif"]})
        msg.add_data({"hchp" : teleinfo["hchp"]})
        msg.add_data({"hchc" : teleinfo["hchc"]})
        msg.add_data({"ptec" : teleinfo["ptec"]})
        msg.add_data({"inst1" : teleinfo["inst1"]})
        msg.add_data({"imax1" : teleinfo["imax1"]})
        msg.add_data({"papp" : teleinfo["papp"]})

        try:
            self.myxpl.send(msg)
        except XplMessageError: 
            self.log.debug(u"Bad xpl message to send. Xpl message is : {0}".format(str(msg)))
            pass

if __name__ == "__main__":
    TimysqlManager()


