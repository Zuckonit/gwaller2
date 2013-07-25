#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
#=============================================================================
#     FileName: diandian.py
#         Desc: Diandian
#       Author: Mocker
#        Email: Zuckerwooo@gmail.com
#     HomePage: zuckonit.github.com
#      Version: 0.0.1
#   LastChange: 2013-05-04 21:27:26
#      History:
#=============================================================================
'''

import re
import os
import time
import sys
try: import simplejson as json
except ImportError: import json
import logger
import smartreq
#import imagebed
__all__ = ['Diandian']

#constants
#====== links =======
URL = {
    'login' : 'http://www.diandian.com/login',
    'logout': 'http://www.diandian.com/logout?formKey=',
    'token' : 'http://www.diandian.com/image/token',
    'upload': 'http://www.diandian.com/upload',
    'check' : 'http://www.diandian.com/check_if_blog_url_is_available?',
    'create_box':'http://www.diandian.com/new/blog',
    'autosave': 'http://www.diandian.com/autosave/save',
    'host': 'www.diandian.com',
    'origin': 'http://www.diandian.com'
}

#======= regex =======
PARSE_FORM_KEY = re.compile(r"window.DDformKey = '(.*?)'")
PARSE_USER_ID  = re.compile(r"ENV.tempUserId = '(.*?)';")
PARSE_USER_ID  = re.compile(r"ENV.tempUserId = '(.*?)';")
PARSE_BOXES_DICT = re.compile(r'<li id="nav-blog-(.*?)" class="blog-item" notify="" url="(.*?)">')

#=======  SNS  =======
SNS = [
    None,   #SNS[0] means no sync to other sns
    'syncToWeibo',
    'syncToQqWeibo',
    'syncToDouban',
    'syncToQzone',
    'syncToRenren',
    'syncToFacebook',
    'syncToTwitter',
    'syncToFlickr'
]

#======= Item ========
BASE_LINK = 'http://www.diandian.com/dianlog/'
ITEM_LINKER = {
        'link' :lambda box_name:BASE_LINK + box_name + '/new/link',
        'photo':lambda box_name:BASE_LINK + box_name + '/new/photo',
        'text' :lambda box_name:BASE_LINK + box_name + '/new/text',
        'audio':lambda box_name:BASE_LINK + box_name + '/new/audio',
        'video':lambda box_name:BASE_LINK + box_name + '/new/video'
}

#====== Diandian class ========
class Diandian(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.req = smartreq.Req(nline=8, nchar=30)
        self.__login_status = 0

    def _login(self):
        postdata = {'account':self.username,'password':self.password,'persistent':1}
        jmp = self.req._open(URL['login'], post_args=postdata)
        self.login_page = jmp.read()
        if "login-error" in self.login_page:
            return False, "Login failed"
        else:
            self.__login_status = 1
            self.formKey = self._get_formkey()
            return True, "Login successfully"

    def _logout(self):
        if self.__login_status == 1:
            self.req._open(URL['logout'])

    def _regex_from_page(self, regex, page):
        return regex.findall(page)

    def _regex_from_login_page(self, regex):
        return self._regex_from_page(regex, self.login_page)

    def _get_formkey(self):
        return self._regex_from_login_page(PARSE_FORM_KEY)[0]

    def _get_boxes_name(self):
        L = self._regex_from_login_page(PARSE_BOXES_DICT)
        L = [(j, i) for (i, j) in L] #swap the key and value
        return dict(L) or {}

    def _get_box_id(self, box_name):
        """return -1 means no such box"""
        return self._get_boxes_name().get(box_name, -1)

    def _get_user_id(self, box_name):
        page = self.req._open(ITEM_LINKER['photo'](box_name)).read()
        return self._regex_from_page(PARSE_USER_ID, page)[0]

    def _get_dtid(self):
        return self.req.get_cookie_item('dtid')

    def _get_token(self, box_name):
        header = {'Referer' :ITEM_LINKER['photo'](box_name)}
        jump = self.req._open(URL['token'], post_args={'formKey':self.formKey}, header=header)
        return jump.read()

    def _sync_post_args(self, post_args={}, opt_syncs='0'):
        """update the postdata when sync set"""
        if opt_syncs == '0':
            return post_args
        for opt in opt_syncs:
            post_args.update({SNS[int(opt)]:'true'})
        return post_args

    def _json_dict(self, jump):
        return json.load(jump) or {}

    def _post_factory(self, item, box_name, postdata, opt_syncs='0', header={}):
        """This is a factory method of post"""
        url = ITEM_LINKER[item](box_name)
        header.update({'Referer':url})
        postdata = self._sync_post_args(postdata, opt_syncs)
        jmp = self.req._open(url, post_args=postdata, header=header)
        return self._json_dict(jmp)

    def _upload_image(self, box_name, img, opt_syncs='0', header={}):
        """Upload image to diandian server"""
        img = os.path.expanduser(img)
        bsname = os.path.basename(img)
        fields = (
            ('Filename',bsname),
            ('publisherBlogId',self._get_box_id(box_name)),
            ('publisherTempUserId',self._get_user_id(box_name)),
            ('imgsize','s100'),
            ('dtid',self._get_dtid()),
            ('tt',self._get_token(box_name).rstrip('\n')),
            ('Filedata',[img]),
            ('Upload','Submit Query')
        )
        header.update({
                        'Referer':ITEM_LINKER['photo'](box_name),
                        'Origin':URL['origin'],
                        'Host':URL['host']
                        })
        return self.req.post_multipart(URL['upload'], header, *fields)

    def post_link(self, box_name,link='#' ,title='', desc='',
                        tags='gwaller,wallpaper', opt_syncs='0', header={}):
        postdata = {
            'formKey':self.formKey,
            'title':title,
            'link':link,
            'desc':'<p>' + desc + '<br /></p>',
            'tags':tags,
            'creativeCommonsType':'by_nc_nd',
            'privacy':0
        }
        return self._post_factory('link',box_name, postdata, opt_syncs,header)


    def post_text(self, links, box_name=None ,title='gwaller', desc='',
                        tags='gwaller,wallpaper', opt_syncs='0', header={}):
        if box_name is None:
            box_name = self._get_boxes_name().keys()[0]
        out = ''
        for link in links[:-1]:
            out += '<p><a href="%s">%s</a></p>'%(link,link)
        out += '<p><a href="%s">%s</a><br /></p>'%(links[-1],links[-1])
        print out
        postdata = {
            'formKey':self.formKey,
            'title':title,
            'content':out,
            'desc':'<p>' + desc + '<br /></p>',
            'tags':tags,
            'creativeCommonsType':'by_nc_nd',
            'privacy':0
        }
        logger.logit('Post %s to %s'%(';'.join(links),box_name))
        return self._post_factory('text',box_name, postdata, opt_syncs,header)

    def post_image(self, image, box_name=None, link=None,opt_syncs=None,
                   header={}):
        if box_name is None:
            box_name = self._get_boxes_name().keys()[0]  #if no box_name given, use the first as default
        if link is None:
            link = 'http://%s.diandian.com' % box_name
        if opt_syncs is None:
            opt_syncs='0'

        jsn = self._json_dict(self._upload_image(box_name, image, opt_syncs, header))
        _id, _url = jsn['id'], jsn['url']
        desc = '<img src="%s" id="%s" />'%(_url, _id)
        out = self._json_dict(self.post_link(box_name, link, desc=desc))
        #may need verification code
        suc = out.get("publisherAfterTipsPortlet",None)
        logger.logit('post image %s to %s'%(image, box_name))  #log
        if suc is not None:
            return out
        else:
            #get the verification code, before that generate the link of verification code
            #show it on qt dialog (UI)
            #use local program to open it
            #input it and post again
            pass

    #below is some interfaces
    def post_audio(self, msg, box_name=None):
        pass

    def post_video(self):
        pass

    def __del__(self):
        self._logout()


#------------- command line -------------#
def opt(arg):
    import optparse
    parser = optparse.OptionParser(usage="usage: %prog [options] [image, [blog_name (the first blog as default)]]")
    parser.add_option(
        "-u","--username",
        dest="_usr",type="string",
        help="your diandian username"
    )
    parser.add_option(
        "-p", "--password",
        dest="_pwd",type="string",
        help="your password of diandiad"
    )
    parser.add_option(
        "-i", "--image",
        dest="_image", type="string",
        help="post image to diandian"
    )
    parser.add_option(
        "-b", "--box",
        dest="_box", type="string",
        help="upload image to special box in diandian"
    )
    parser.add_option(
        "-s", "--sync",
        dest="_sync", type="string",
        help="""sync your information to other sns (set the sync on website by yourself)
                1:syncToWeibo
                2:syncToQqWeibo
                3:syncToDouban
                4:syncToQzone
                5:syncToRenren
                6:syncToFacebook
                7:syncToTwitter
                8:syncToFlickr
        """
    )
    parser.add_option(
        "-l", "--link",
        dest="_link", type="string",
        help="add link to image"
    )
    parser.add_option(
        "-v", "--verbose",
        dest="_vbose", action="store_true", default=False,
        help="show the output of result"
    )
    (options, args) = parser.parse_args(arg)
    _usr,_pwd,_image,_box,_sync,_link,_ver = (
                                              options._usr,
                                              options._pwd,
                                              options._image,
                                              options._box,
                                              options._sync,
                                              options._link,
                                              options._vbose
                                              )
    if _usr and _pwd and _image:
        diandian = Diandian(_usr,_pwd)
        diandian._login()
        out = diandian.post_image(_image,_box, _link, _sync)
        print out if _ver is not None else ''
    else:
        print "type %s -h to get help" % (os.path.basename(sys.argv[0]))

def _test():
    import config
    username = config.ACCOUNT['username']
    password = config.ACCOUNT['password']
    demo = Diandian(username, password)
    demo._login()
    #print demo.post_image('gwaller','1.jpg')
    print demo.post_text("http://baidu.com").read()

if __name__ == '__main__':
    _test()
    #opt(sys.argv)
