#!/usr/bin/env python
#-*- coding:utf-8  -*-
'''
#=============================================================================
#     FileName: wallpaper.py
#         Desc: wallpaper
#       Author: Mocker
#        Email: Zuckerwooo@gmail.com
#     HomePage: zuckonit.github.com
#      Version: 0.0.1
#   LastChange: 2013-05-04 21:28:37
#      History:
#=============================================================================
'''

import os
import glob
import gconf
import time

import errors
import conf
import logger

fmt=('jpg','png','bmp','jpeg')
class XML(object):
    def __init__(self, xml):
        self.xml = xml

    def read_xml(self, mode='rb'):
        f = open(self.xml, mode)
        data = f.read()
        f.close()
        return data

    def write_xml(self, mode='wb'):
        data = self._register_xml()
        try:
            f = open(self.xml, mode)
            f.write(data)
            f.close()
            return True
        except:
            return False

    def encode_xml(self, escaped):
        unescaped = escaped.replace('&amp;', '&')
        unescaped = unescaped.replace('&apos;', "'")
        unescaped = unescaped.replace('&quot;', '"')
        unescaped = unescaped.replace('&lt;', '<')
        unescaped = unescaped.replace('&gt;', '>')
        return unescaped

    def _register_xml(self, kw=conf.GNOME2['default']):
        fname = os.path.basename(self.xml)
        wp_insert = """
        <wallpaper deleted="false">
            <name>{0}</name>
            <filename>{1}</filename>
            <options>{2}</options>
            <shade_type>{3}</shade_type>
            <pcolor>{4}</pcolor>
            <scolor>{5}</scolor>
        </wallpaper>
        </wallpapers>""".format(self.encode_xml(fname),
                                self.encode_xml(self.xml),
                                kw['style'],
                                kw['shade'],
                                kw['pcolor'],
                                kw['scolor'])
        xml_data = self.read_xml()
        return xml_data.replace('</wallpapers>', xml_data)


class Wall(object):
    def __init__(self, xml, kw=conf.GNOME2['default']):
        self.xml = xml
        self.style = kw['style']

    def _set_wallpaper(self):
        try:
            client = gconf.client_get_default()
        except:
            raise errors.Err(errors.ECGCFCREAT,errors.ENGCFCREAT,errors.MSGCFCREAT)
        else:
            if not client.set_string("/desktop/gnome/background/picture_filename",
                                     self.xml):
                logger.logit(errors.MSGCFSETWP)
                raise errors.WallGconfError(errors.ECGCFSETWP,
                                            errors.ENGCFSETWP,
                                            errors.MSGCFSETWP)
            else:
                if not client.set_string('/desktop/gnome/background/picture_options',
                                         self.style):
                    logger.logit(errors.MSGCFWPSTY)
                    raise errors.WallGconfError(errors.ECGCFWPSTY,
                                                errors.ENGCFWPSTY,
                                                errors.MSGCFWPSTY)
                return True
        return False


class _XML(object):
    def __init__(self, imgs,
                 duration=conf.GNOME2['default']['duration'],
                 interval=conf.GNOME2['default']['interval']):
        if not isinstance(imgs, list):
            if os.path.isfile(imgs):
                self.imgs = list(imgs)
            elif os.path.isdir(imgs):
                imgs = os.path.expanduser(imgs)
                if not imgs.endswith('/'):
                    imgs += '/'
                self.imgs = []
                for ext in fmt:
                    self.extend(glob.glob(imgs + '*.' + ext))

        self.imgs = imgs
        self.dur  = duration
        self.inte = interval
        print imgs
        print duration
        print interval

    def _gen_header(self):
        year  = time.strftime("%Y")
        month = time.strftime("%m")
        day   = time.strftime("%d")
        hour  = time.strftime("%H")
        min   = time.strftime("%M")
        sec   = time.strftime("%S")

        header = """
        <background>
            <starttime>
                <year>{0}</year>
                <month>{1}</month>
                <day>{2}</day>
                <hour>{3}</hour>
                <minute>{4}</minute>
                <second>{5}</second>
        </starttime> """.format(year,month,day,hour,min,sec)
        return header

    def _gen_body(self):
        xml="""
        <static>
            <duration>{0}</duration>
            <file>{1}</file>
        </static>
        <transition>
            <duration>{2}</duration>
            <from>{3}</from>
            <to>{4}</to>
        </transition>"""
        body, count = '', len(self.imgs)
        for i in xrange(count):
            body += xml.format(self.dur,self.imgs[i],self.inte,
                               self.imgs[i],self.imgs[(i+1)%count])
        return body

    def _gen_footer(self):
        return """"
                </background>"""

    def gen_xml(self):
        return self._gen_header() + self._gen_body() + self._gen_footer()

    def save_xml(self):
        xml = self.gen_xml()
        import hashlib      #lazy import
        m = hashlib.md5()
        m.update(xml)
        md5_name = m.hexdigest()
        save_dir = conf.DIRS.get('xdir',os.path.expanduser('~/.gwaller/xmls'))
        xml_name = "%s/%s.xml"%(save_dir, md5_name)
        if not os.path.exists(xml_name):
            f = open(xml_name,'wb')
            f.write(xml)
            f.close()
        return xml_name

    def register_xml(self):
        xml_path = self.save_xml()
        xml = XML(xml_path)
        return xml_path

    def setWallpaper(self):
        xml = self.register_xml()
        wall = Wall(xml)
        wall._set_wallpaper()

