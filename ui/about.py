# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Wed May  1 17:27:53 2013
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(414, 263)
        Dialog.setMinimumSize(QtCore.QSize(414, 263))
        Dialog.setMaximumSize(QtCore.QSize(414, 263))
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.horizontalLayoutWidget = QtGui.QWidget(self.splitter)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.commandLinkButton = QtGui.QCommandLinkButton(self.horizontalLayoutWidget)
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.horizontalLayout.addWidget(self.commandLinkButton)
        self.btnAboutExit = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnAboutExit.setObjectName("btnAboutExit")
        self.horizontalLayout.addWidget(self.btnAboutExit)
        self.verticalLayout.addWidget(self.splitter)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.btnAboutExit, QtCore.SIGNAL("clicked()"), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Software: Gwaller</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Version:  0.0.1</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Author: Yang Yiming</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Blog: <a href=\"zuckonit.github.com\"><span style=\" text-decoration: underline; color:#0000ff;\">zuckonit.github.com</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Email: <a href=\"mailto:Zuckerwooo@gmail.com\"><span style=\" text-decoration: underline; color:#0000ff;\">Zuckerwooo@gmail.com</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.commandLinkButton.setText(QtGui.QApplication.translate("Dialog", "Software page", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAboutExit.setText(QtGui.QApplication.translate("Dialog", "Exit", None, QtGui.QApplication.UnicodeUTF8))

