#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import MySQLdb as mdb

NETWORK = [
    {'ip': 'ADD_IP', 'name': 'ADD_NAME'},
    {'ip': 'ADD_IP', 'name': 'ADD_NAME'},
    {'ip': 'ADD_IP', 'name': 'ADD_NAME'},
    {'ip': 'ADD_IP', 'name': 'ADD_NAME'},
    {'ip': 'ADD_IP', 'name': 'ADD_NAME'}
]

con = mdb.connect('HOST', 'USERNAME', 'PASSWORD', 'DATABASE')
cur = con.cursor()

with con:
    for hostname in NETWORK:
        response = os.system("ping -c 1 -n -W 2 " + hostname['ip'])
        if response == 0:
            cur.execute("INSERT INTO network(ip, name, status, created) VALUES ('" + hostname['ip'] + "', '" + hostname['name'] + "', 'up', now() ) ")
        else:
            cur.execute("INSERT INTO network(ip, name, status, created) VALUES ('" + hostname['ip'] + "', '" + hostname['name'] + "', 'down', now() ) ")

#CREATE TABLE `network` (
#  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
#  `ip` varchar(100) DEFAULT NULL,
#  `name` varchar(255) DEFAULT NULL,
#  `status` varchar(11) DEFAULT '',
#  `created` datetime DEFAULT NULL,
#  PRIMARY KEY (`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
