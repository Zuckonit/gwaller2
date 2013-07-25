#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import conf
import hashlib

__all__ = ['Qrcode']

try:
    import qrcode
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__),'other'))
    import qrcode

QRCODE_TMP_DIR = conf.DIRS.get('qrDir',os.path.expanduser('~/.gwaller/qrcode'))

class Qrcode(object):
    def __init__(self, msg):
        m = hashlib.md5()
        m.update(msg)
        self.fname = m.hexdigest()
        self.im = qrcode.make(msg)

    def save(self, sdir=None):
        if sdir is None: sdir = QRCODE_TMP_DIR
        _n = "%s.png" % self.fname
        _s = os.path.join(sdir, _n)
        if not os.path.exists(_s):
            self.im.save(_s)
        return _s

#------------- command line -------------#
def opt(arg):
    import optparse
    parser = optparse.OptionParser(usage="usage: %prog [options] [msg, [save_dir (/tmp/)]]")
    parser.add_option(
        "-m", "--message",
        dest="_msg", type="string",
        help="the message that you wanna make into your qrcode"
    )
    parser.add_option(
        "-s", "--save-dir",
        dest="_sdir", type="string",
        help="the directory you wanna put your qrcode into"
    )
    parser.add_option(
        "-v", "--verbose",
        dest="_vbose", action="store_true", default=False,
        help="show the output of result"
    )
    (options, args) = parser.parse_args(arg)

    _msg, _sdir, _vbose = options._msg, options._sdir, options._vbose
    if _msg is not None:
        code = Qrcode(_msg)
        out  = code.save(_sdir)
        print out if _vbose is not None else ""
    else:
        print "type %s -h to get help" % os.path.basename(sys.argv[0])

if __name__ == '__main__':
    opt(sys.argv)

