#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import urllib

URL = "http://cn.bing.com"
PARSE_IMG = re.compile(r"g_img={url:'(.*?)'", re.DOTALL)

def download():
    page = urllib.urlopen(URL).read()
    link = PARSE_IMG.findall(page)[0]
    return link, link.split('/')[-1]

if __name__ == '__main__':
    print download()
