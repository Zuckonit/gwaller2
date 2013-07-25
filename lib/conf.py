#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

DIRS = {
    'rdir':os.path.expanduser('~/.gwaller'),
    'xdir':os.path.expanduser('~/.gwaller/xmls'),
    'colorDir':os.path.expanduser('~/.gwaller/colors'),
    'bingDir':os.path.expanduser('~/.gwaller/bing'),
    'cfgDir':os.path.expanduser('~/.gwaller/conf'),
    'qrDir':os.path.expanduser('~/.gwaller/qrcode'),
}

FILES = {
    'logfile':os.path.expanduser('~/.gwaller/logs'),
}

ACCOUNT = {
    'username':'lsin30@foxmail.com',
    'password':'yang3136299',
}


#create dirs
for k,v in DIRS.items():
    if not os.path.exists(v):
        os.makedirs(v)

MAX_PIC_COUNT = 10    #max pic count allowed to be added
GNOME2 = {
    'default':{
        'duration':1795.0,
        'interval':5.0,
        'style' :'zoom',
        'pcolor':'#2c2c00001e1e',
        'scolor':'#2c2c00001e1e',
        'shade' :'solid',
    }
}
