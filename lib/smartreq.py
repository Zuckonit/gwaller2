#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
#=============================================================================
#     FileName: smartreq.py
#         Desc: this is a base class of Request
#       Author: Mocker
#        Email: Zuckerwooo@gmail.com
#     HomePage: zuckonit.github.com
#      Version: 0.0.1
#   LastChange: 2013-05-04 21:27:48
#      History:
#=============================================================================
'''

import urllib
import urllib2
import cookielib
import base64
import uuid
import os

TIMEOUT = 10
CONTENT_TYPE_DFEAULT = 0
CONTENT_TYPE_SUFFIX  = 1

class Req(object):
    def __init__(self, nline=10, nchar=30):
        self.nline = nline
        self.nchar = nchar
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)
        urllib2.build_opener()

    def _open(self, url, get_args=None, post_args=None, header={}, timeout=TIMEOUT):
        header.update({
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31'
        })
        if get_args is not None:
            url = '%s?%s' % (url, urllib.urlencode(get_args))
        if post_args is not None:
            if isinstance(post_args, dict):
                post_args = urllib.urlencode(post_args)
            req = urllib2.Request(url, post_args, header)
        else:
            req = urllib2.Request(url)
        return self.opener.open(req,timeout=TIMEOUT)

    def post_url(self, url, postdata, header={}):
        return self._open(url, post_args=postdata, header=header)

    def get_url(self, url, getdata, header={}):
        return self._open(url, get_args=getdata, header=header)

    def get_cookie_item(self, item):
        for c in self.cj:
            if c.name == item:return c.value

    def _update_dict(self, src, dst):
        kw = src.copy()
        kw.update(dst)
        return kw

    def gen_boundary(self):
        _uuid = uuid.uuid1()
        return '-' * self.nline + base64.encodestring(str(_uuid))[:self.nchar]

    def get_content_type(self, fp, method=CONTENT_TYPE_DFEAULT):
        if method == CONTENT_TYPE_DFEAULT:
            return 'application/octet-stream'
        else:
            fmt = {
                    'png':'image/png',
                    'jpg':'image/jpeg',
                    'jpeg':'image/jpeg',
                    'jpe':'image/jpeg',
                    'gif':'image/gif',
                    'bmp':'image/bmp'
            }
            ext = fp.lower().split('.')[-1]
            content_type = fmt.get(ext,None)
            return content_type or 'application/octet-stream'

    def encode_multipart(self, *kw):
        boundary = self.gen_boundary()
        CRFL, L = '\r\n', []
        for (k, v) in kw:
            L.append('--%s' % boundary)
            if isinstance(v, list):
                fname = os.path.basename(v[0])
                f = open(os.path.expanduser(v[0]), 'rb')
                data = f.read()
                f.close()
                L.append('Content-Disposition: form-data; name="%s"; filename="%s"'%(k, fname))
                L.append('Content-Type: %s\r\n'%self.get_content_type(v[0],method=1))
                L.append(data)
            else:
                L.append('Content-Disposition: form-data; name="%s"\r\n' %(k))
                L.append(v.encode('utf-8') if isinstance(v, unicode) else v)

        L.append('--%s--' % boundary)
        body = CRFL.join(L)
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return body, content_type

    def post_multipart(self, url, header={}, *kw):
        postdata, content_type = self.encode_multipart(*kw)
        header.update({'Content-Type':content_type})
        return self.post_url(url, postdata, header)


#>>>>>> This is for test <<<<<<<
def main():
    user = ''  #your diandian username
    pawd = ''  #your diandian password
    url = 'http://www.diandian.com/login'
    postdata = {
        'account': user,
        'password': pawd,
        'persistent': 1
    }
    demo = Req()
    jmp = demo._open(url, post_args=postdata)
    print jmp.read()

if __name__ == '__main__':
    main()
