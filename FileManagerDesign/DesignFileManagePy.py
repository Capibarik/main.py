# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DesignFileManager.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PySide6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 510, 781, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnStart = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnStart.setIconSize(QtCore.QSize(16, 16))
        self.btnStart.setObjectName("btnStart")
        self.horizontalLayout.addWidget(self.btnStart)
        self.btnChangePanel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnChangePanel.setObjectName("btnChangePanel")
        self.horizontalLayout.addWidget(self.btnChangePanel)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 781, 491))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.panelDynamic = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        self.panelDynamic.setFrameShape(QtWidgets.QFrame.Box)
        self.panelDynamic.setFrameShadow(QtWidgets.QFrame.Raised)
        self.panelDynamic.setLineWidth(1)
        self.panelDynamic.setObjectName("panelDynamic")
        self.horizontalLayout_2.addWidget(self.panelDynamic)
        self.panelStatic = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        self.panelStatic.setFrameShape(QtWidgets.QFrame.Box)
        self.panelStatic.setFrameShadow(QtWidgets.QFrame.Raised)
        self.panelStatic.setLineWidth(1)
        self.panelStatic.setMidLineWidth(0)
        self.panelStatic.setObjectName("panelStatic")
        self.horizontalLayout_2.addWidget(self.panelStatic)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnStart.setText(_translate("MainWindow", "Открыть"))
        self.btnChangePanel.setText(_translate("MainWindow", "Сменить панель"))