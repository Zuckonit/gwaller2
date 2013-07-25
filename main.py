#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
#=============================================================================
#     FileName: main.py
#         Desc:
#       Author: Mocker
#        Email: Zuckerwooo@gmail.com
#     HomePage: zuckonit.github.com
#      Version: 0.0.1
#   LastChange: 2013-05-04 21:23:51
#      History:
#=============================================================================
'''
import sys
import os
import getpass
import webbrowser
import urllib
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *

sys.path.append(os.path.abspath(os.path.dirname(__file__) + './ui'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + './lib/other'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + './lib'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + './lib/plugin'))
from gui import Ui_MainFrame
import about
import login
import preview
import pam
import wallpaper
import conf
import bing

import diandian
import imagebed
import notify
import qrcodewrapper

__software_link__ = 'http://zuckonit.github.com'
__help_link__ = 'http://zuckonit.github.com'


MAX_COUNT = conf.MAX_PIC_COUNT
def openLink(link):
    webbrowser.open_new_tab(link)

print conf.ACCOUNT['username']
print conf.ACCOUNT['password']

class UploadDialog(QtGui.QDialog):
    def __init__(self):
        super(UploadDialog, self).__init__()
        self.initUI()
        self.imgList = []
        self.curItem = 0
        self.links = []
        self.setModal(True)
        self.dd = diandian.Diandian(conf.ACCOUNT['username'], conf.ACCOUNT['password'])
        self.dd._login()
        self.post_type = 0

    def initUI(self):
        self.pbar = QtGui.QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.button = QtGui.QPushButton('Start', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(40, 80)
        self.connect(self.button, QtCore.SIGNAL('clicked()'),
            self.doAction)
        self.timer = QtCore.QBasicTimer()
        self.setWindowTitle('Uploading...')
        self.setGeometry(300, 300, 250, 150)


    def timerEvent(self, event):
        self.pbar.setMaximum(len(self.imgList))
        if self.curItem >= len(self.imgList):
            if self.post_type == 1:
                t = self.dd.post_text(self.links)
                print t
            elif self.post_type == 2:
                qr_content = '\r\n'.join(self.links)
                image = qrcodewrapper.Qrcode(qr_content).save()
                t = self.dd.post_image(image)
                print t
            self.timer.stop()
            if t.has_key('result'):
                notify.Notify(t['result'])
            self.close()
            return
        #here upload your image
        ibed = imagebed.ImgBed(str(self.imgList[self.curItem]))
        link = ibed.upload()
        self.links.append(link)
        self.curItem += 1
        self.pbar.setValue(self.curItem)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.button.setText('Start')
        else:
            self.timer.start(100, self)
            self.button.setText('Stop')

class LoginDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = login.Ui_Dialog()
        self.ui.setupUi(self)
        user = '''<html><head/><body><p><span style=" font-size:18pt; font-weight:600; color:#0000ff;">%s</span></p></body></html>'''%self.getUsername()
        self.ui.labUsername.setText(user)

        self.verifyTime = 0
        self.connect(self.ui.btnLogin, QtCore.SIGNAL("clicked()"), self.verify)

        self.imgList = []
        self.slideDur = 150
        self.transInterval = 2.0

    def getUsername(self):
        return getpass.getuser()

    def setWallpaper(self):
        xml = wallpaper._XML(self.imgList,self.slideDur, self.transInterval)
        xml.setWallpaper()

    def verify(self):
        self.verifyTime += 1
        import pam
        password = self.ui.editPassword.text()
        status =  pam.authenticate(self.getUsername(), password)
        if not status:
            self.ui.labStatus.setText("Validate failed %d"%self.verifyTime)
            self.ui.editPassword.clear()
        else:
            self.ui.labStatus.setText("Validate passed")
            self.setWallpaper()
            notify.Notify(title='gwaller',content="set wallpaper successful").inotify()
            self.close()


class AboutDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = about.Ui_Dialog()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.commandLinkButton, QtCore.SIGNAL("clicked()"), self.openSoftwarePage)

    def openSoftwarePage(self):
        openLink(__software_link__)


class Preview(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = preview.Ui_MainWindow()
        self.ui.setupUi(self)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.width  = screen.width()
        self.height = screen.height()
        self.move(0, 0)
        #set minum width and height
        self.setMinimumWidth(self.width)
        self.setMinimumHeight(self.height)
        #resize the window when open
        self.resize(self.width, self.height)
        self.curIndex = 0
        self.imgList = QtCore.QStringList([])

    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Right or event.key()==QtCore.Qt.Key_Space:
            self.curIndex += 1
        elif event.key()==QtCore.Qt.Key_Left:
            self.curIndex -= 1
        self.curIndex %= len(self.imgList)
        self.setImage()

    def getPixmap(self, img):
        if os.path.isfile(unicode(img)):
            pixmap = QtGui.QPixmap(img)
            pixmap = pixmap.scaled(self.width, self.height)
            return pixmap
        return img

    def setImage(self):
        pixmap = self.getPixmap(self.imgList[self.curIndex])
        self.ui.labImage.clear()
        self.ui.labImage.setPixmap(pixmap)
        self.setWindowTitle(str(self.curIndex+1))   #set current slide as the window title


class MyFrame(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyFrame,self).__init__(parent)
        self.ui = Ui_MainFrame()
        self.ui.setupUi(self)

        #size of your screen
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.width  = screen.width()
        self.height = screen.height()
        self.resize(self.width, self.height)
        #self.ui.listWidget.setStyleSheet('''background-color:black;''')
        #Bottom Button
        self.connect(self.ui.btnAddSlide, QtCore.SIGNAL("clicked()"), self.addSlide)
        self.connect(self.ui.btnDelSlide, QtCore.SIGNAL("clicked()"), self.deleteSlide)
        self.connect(self.ui.btnSure, QtCore.SIGNAL("clicked()"), self.loginDialog)
        self.connect(self.ui.btnPreview, QtCore.SIGNAL("clicked()"), self.previewDialog)
        self.connect(self.ui.comboxPlugin, QtCore.SIGNAL("currentIndexChanged(int)"), self.downloadDialog)
        self.connect(self.ui.comboxDiandian, QtCore.SIGNAL("currentIndexChanged(int)"), self.uploadDialog)

        #QListWidget
        self.connect(self.ui.listWidget, QtCore.SIGNAL("itemDoubleClicked (QListWidgetItem *)"), self.deleteSlide)
        ##right click menu
        self.contextMeunuEvent()

        #QDial
        self.connect(self.ui.DialSlideDur, QtCore.SIGNAL("valueChanged(int)"), self.setSlideDur)
        self.connect(self.ui.DialTransDur, QtCore.SIGNAL("valueChanged(int)"), self.setTransDur)

        #menu
        ##File
        self.connect(self.ui.actionOpen, QtCore.SIGNAL("triggered()"), self.addSlide)
        self.connect(self.ui.actionExit, QtCore.SIGNAL("triggered()"), self.close)

        ##Help
        self.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered()"), self.aboutDialog)
        self.connect(self.ui.actionContent, QtCore.SIGNAL("triggered()"), self.openHelpPage)

        ##setting
        self.connect(self.ui.actionDiandian, QtCore.SIGNAL("triggered()"), self.accountDialog)

        #init the dialog
        self.preview = Preview(parent=self)
        self.login = LoginDialog(parent=self)
        self.dlg_upload = UploadDialog()

    #------------QDial-------------#
    def setSlideDur(self, num):
        self.ui.labSlideDur.setNum(num)

    def setTransDur(self, num):
        self.ui.labTransDur.setNum(num/10.0)

    def getSlideDur(self):
        return int(self.ui.labSlideDur.text())

    def getTransDur(self):
        return float(self.ui.labTransDur.text())

    #-----------QLCD---------------#
    def picCounter(self):
        nItems = self.getPicCount()
        self.ui.lcdPictures.display(nItems)

    #------function for listWidget------#
    ##right click menu
    def contextMeunuEvent(self):
        """this is for right click menu"""
        self.ui.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.listWidget.customContextMenuRequested.connect(self.showContextMenu)

        self.contextMenu = QtGui.QMenu(self)
        self.actionAdd = self.contextMenu.addAction('Add Slide')
        self.actionDel = self.contextMenu.addAction('Del Slide')
        self.solidColor= self.contextMenu.addAction('Pure Color')

        self.actionAdd.triggered.connect(self.addSlide)
        self.actionDel.triggered.connect(self.deleteSlide)
        self.solidColor.triggered.connect(self.colorDialog)

    def showContextMenu(self, pos):
        self.contextMenu.move(self.pos() + pos)
        self.contextMenu.show()

    ##get the item number in listWidget
    def getPicCount(self):
        return self.ui.listWidget.count()

    ##add slides
    def addPixmap(self, pixmap):
        item = QListWidgetItem()
        icon = QIcon(pixmap)
        item.setIcon(icon)
        self.ui.listWidget.addItem(item)

    def _addFileToList(self, filename):
        if not filename.isEmpty():
            pixmap = QtGui.QPixmap(filename)
            pixmap = pixmap.scaled(200,140)
            self.addPixmap(pixmap)
        self.picCounter()

    def addSlide(self):
        files = QtGui.QFileDialog.getOpenFileNames(self, 'Add slide', os.path.expanduser("~"), "Image Files (*.png *.jpg *.bmp *.jpeg)")
        files = files[:MAX_COUNT]   #limit the max count
        for f in files:
            self._addFileToList(f)
            self.preview.imgList.insert(0,f)
        return files

    ##delete slides
    def deleteSlide(self):
        selectedList = self.ui.listWidget.selectedItems()
        for i in selectedList:
            index = self.ui.listWidget.row(i)
            self.ui.listWidget.takeItem(index)
            self.preview.imgList.removeAt(index)
        self.picCounter()

    #------------exact dialogs----------------#
    def accountDialog(self):
        myapp = AccountDialog(parent=self)
        myapp.show()

    def loginDialog(self):
        if len(self.preview.imgList) < 1:
            self.ui.statusbar.showMessage('Error: one picture at lest!')
            notify.Notify('Error: one picture at lest!')
            return
        self.login.show()
        self.login.imgList = list(self.preview.imgList)
        self.login.slideDur = self.getSlideDur()
        self.login.transInterval = self.getTransDur()

    def aboutDialog(self):
        myapp = AboutDialog(parent=self)
        myapp.show()

    def previewDialog(self):
        self.preview.curIndex = 0
        if len(self.preview.imgList) < 1:
            self.ui.statusbar.showMessage("Error: no picture to be previewed!!!")
            notify.Notify('Error: no picture to be previewed!!!!')
            return
        self.preview.show()
        self.preview.setImage()

    def colorDialog(self):
        col = QtGui.QColorDialog.getColor()
        cname = col.name()
        pixmap = QPixmap(200,140)
        pixmap = QPixmap(self.width,self.height)
        pixmap.fill(QColor(cname))
        save_name = conf.DIRS.get('colorDir', os.path.expanduser("~/.gwaller/colors")) + '/' +  cname + '.png'
        if not os.path.exists(save_name):
            pixmap.save(save_name)
        self._addFileToList(save_name)
        self.preview.imgList.insert(0, save_name)
        return save_name

    def downloadDialog(self):
        curItem = self.ui.comboxPlugin.currentIndex()
        fname = ''
        if curItem == 1:
            link, fname = bing.download()
        save_name = conf.DIRS.get('bingDir', os.path.expanduser('~/.gwaller/bing')) + '/' + fname
        if not os.path.exists(save_name):
            urllib.urlretrieve(link, save_name)
        save_name = QtCore.QString(save_name)
        self._addFileToList(save_name)
        self.preview.imgList.insert(0, save_name)
        return save_name

    def uploadDialog(self):
        curItem = self.ui.comboxDiandian.currentIndex()
        if curItem == 0:
            return
        if len(self.preview.imgList) < 1:
            self.ui.statusbar.showMessage("Error: no picture to be uploaded!!!")
            notify.Notify('Error: no picture to be uploaded!!!')
            return
        self.dlg_upload.pbar.reset()
        self.dlg_upload.show()
        self.dlg_upload.post_type = curItem
        self.dlg_upload.imgList = self.preview.imgList

    #-----------open link in browser----------#
    def openHelpPage(self):
        openLink(__help_link__)

    def openSoftwarePage(self):
        openLink(__software_link__)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    splash = QtGui.QSplashScreen(QtGui.QPixmap('./ui/images/splash.png').scaled(500,400))
    splash.showMessage("Loading...")
    splash.show()
    myapp = MyFrame()
    myapp.show()
    import time
    time.sleep(2)
    splash.finish(myapp)
    sys.exit(app.exec_())
