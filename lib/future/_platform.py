#-*- coding:utf-8 -*-
import commands
import os

def commandstatus(cmd):
    status, output = commands.getstatusoutput("ps -A | grep %s"%cmd)
    return status

def get_platform():
    if os.name == 'nt':
        return "Windows"
    if not commandstatus("gnome-panel") and os.environ.get("DESKTOP_SESSION") == "gnome":
        return "Gnome"
    if not commandstatus("xfce4-panel"):
        return "XFCE"
    if not commandstatus("mate-panel"):
        return "MATE"
    if not commandstatus("lxpanel"):
        return "LXDE"
