#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import sys
from smartreq import Req
import logger

__all__ = [ 'ImgBed' ]

URL = {
    'upload':'http://www.freeimagehosting.net/upload.php',
    'imageporter':'http://www.imageporter.com/',
    'freep':'http://www1.freep.cn/',
    's2':'http://s2.upload.tf/'
}

PARSE_SHARE_LINK = re.compile(r'(http://www.freeimagehosting.net/[^.]+?)"')
QRCODE_TMP_DIR = "/tmp/"

class ImgBed(object):
    def __init__(self, img):
        self.img = os.path.abspath(img)
        self.img = os.path.expanduser(img)
        self.req = Req(nline=4, nchar=34)

    def upload(self):
        header = {
            'Host':'www.freeimagehosting.net',
            'Origin':'http://www.freeimagehosting.net',
            'Referer':'http://www.freeimagehosting.net/upload.php',
        }
        kw  = (('attached',[self.img]))
        jmp = self.req.post_multipart(URL['upload'],header,kw)
        link = PARSE_SHARE_LINK.findall(jmp.read())[0]
        logger.logit('post %s to %s'%(self.img,link))      #log
        return link

#------------- command line -------------#
def opt(arg):
    import optparse
    parser = optparse.OptionParser(usage="usage: %prog [options] [image]")
    parser.add_option(
        "-i", "--image",
        dest="_image", type="string",
        help="upload image to website, and return the share link"
    )

    parser.add_option(
        "-v", "--verbose",
        dest="_vbose", action="store_true", default=False,
        help="show the output of result"
    )
    (options, args) = parser.parse_args(arg)
    _image, _vbose = options._image, options._vbose

    #when add -v|--verbose, then output will be showed
    if _image is not None:
        img = ImgBed(options._image)
        out = img.upload()
        print out if _vbose is not None else "",
    else:
        print "type %s -h to get help" % os.path.basename(sys.argv[0])

if __name__ == '__main__':
   opt(sys.argv)
