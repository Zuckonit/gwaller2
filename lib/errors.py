#*-* coding:utf-8 *-*

ECGCFCREAT = 10000   #error code
ENGCFCREAT = "ErrGconfClientCreat" #error name
MSGCFCREAT = "unable to create gconf client"  #error message

ECGCFSETWP = 10001
ENGCFSETWP = "ErrGconfSetWallpaper"
MSGCFSETWP = "unable to set wallpaper with gconf"

ECGCFWPSTY = 10002
ENGCFWPSTY = "ErrGconfWallpaperStyle"
MSGCFWPSTY = "unable to set wallpaper style with gconf"

class Err(Exception):
    def __init__(self, errcode, errname, errmsg):
        self.errcode = errcode
        self.errname = errname
        self.errmsg  = errmsg

    def __str__(self):
        return "[ %d ]: %s --- %s" % (self.errcode, self.errname, self.errmsg)

    def get_errmsg(self):
        return self.errmsg

    def get_errcode(self):
        return self.errcode

    def get_errname(self):
        return self.errname

    def set_errmsg(self, msg):
        self.errmsg = msg

    def set_errname(self, name):
        self.errname = name

    def set_errcode(self, code):
        self.errcode = code
