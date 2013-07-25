#!/usr/bin/env python
'''
#=============================================================================
#     FileName: notify.py
#         Desc:
#       Author: Mocker
#        Email: Zuckerwooo@gmail.com
#     HomePage: zuckonit.github.com
#      Version: 0.0.1
#   LastChange: 2013-03-12 01:31:20
#      History:
#=============================================================================
'''
import pynotify
import sys

__all__ = ['Notify']

class Notify(object):
    def __init__(self, content, title='gwaller', icon=None):
        n = pynotify.init(sys.argv[0])
        self.nty = pynotify.Notification(title, content, icon)
        self._inotify()

    def _inotify(self):
        self.nty.show()

def _test():
    n = Notify('tst','test')
    n.inotify()

if __name__ == '__main__':
    _test()
