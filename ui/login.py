# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Wed May  1 17:29:52 2013
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(275, 150)
        Dialog.setMinimumSize(QtCore.QSize(275, 150))
        Dialog.setMaximumSize(QtCore.QSize(275, 150))
        Dialog.setModal(True)
        self.btnLogin = QtGui.QCommandLinkButton(Dialog)
        self.btnLogin.setEnabled(True)
        self.btnLogin.setGeometry(QtCore.QRect(160, 110, 160, 110))
        self.btnLogin.setMinimumSize(QtCore.QSize(160, 101))
        self.btnLogin.setMaximumSize(QtCore.QSize(160, 110))
        self.btnLogin.setSizeIncrement(QtCore.QSize(160, 110))
        self.btnLogin.setAutoFillBackground(False)
        self.btnLogin.setObjectName("btnLogin")
        self.editPassword = QtGui.QLineEdit(Dialog)
        self.editPassword.setGeometry(QtCore.QRect(50, 60, 191, 31))
        self.editPassword.setInputMethodHints(QtCore.Qt.ImhNone)
        self.editPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.editPassword.setObjectName("editPassword")
        self.labUsername = QtGui.QLabel(Dialog)
        self.labUsername.setGeometry(QtCore.QRect(50, 10, 211, 31))
        self.labUsername.setTextFormat(QtCore.Qt.RichText)
        self.labUsername.setScaledContents(True)
        self.labUsername.setWordWrap(False)
        self.labUsername.setObjectName("labUsername")
        self.labStatus = QtGui.QLabel(Dialog)
        self.labStatus.setGeometry(QtCore.QRect(20, 115, 131, 31))
        self.labStatus.setText("")
        self.labStatus.setObjectName("labStatus")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Verification", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLogin.setText(QtGui.QApplication.translate("Dialog", "Login", None, QtGui.QApplication.UnicodeUTF8))
        self.labUsername.setText(QtGui.QApplication.translate("Dialog", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600; color:#0000ff;\">username</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

