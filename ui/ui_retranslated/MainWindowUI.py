# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_files/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import ui.resources.resources


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 820)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 1261, 711))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.canvasLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.canvasLayout.setContentsMargins(0, 0, 0, 0)
        self.canvasLayout.setObjectName("canvasLayout")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(100, 10, 1171, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.DrawButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.DrawButton.setObjectName("DrawButton")
        self.horizontalLayout.addWidget(self.DrawButton)
        self.ReflectButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.ReflectButton.setObjectName("ReflectButton")
        self.horizontalLayout.addWidget(self.ReflectButton)
        self.RotateButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.RotateButton.setObjectName("RotateButton")
        self.horizontalLayout.addWidget(self.RotateButton)
        self.ColorButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.ColorButton.setObjectName("ColorButton")
        self.horizontalLayout.addWidget(self.ColorButton)
        self.AlphaButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.AlphaButton.setObjectName("AlphaButton")
        self.horizontalLayout.addWidget(self.AlphaButton)
        self.BlurButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.BlurButton.setObjectName("BlurButton")
        self.horizontalLayout.addWidget(self.BlurButton)
        self.SizeButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.SizeButton.setObjectName("SizeButton")
        self.horizontalLayout.addWidget(self.SizeButton)
        self.QuantizeButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.QuantizeButton.setObjectName("QuantizeButton")
        self.horizontalLayout.addWidget(self.QuantizeButton)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 81, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.MainColor = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.MainColor.setText("")
        self.MainColor.setObjectName("MainColor")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.MainColor)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.SecondaryColor = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.SecondaryColor.setText("")
        self.SecondaryColor.setObjectName("SecondaryColor")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.SecondaryColor)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_2.addLayout(self.formLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.LastForms = QtWidgets.QMenu(self.menufile)
        self.LastForms.setObjectName("LastForms")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/rec/resources/open_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_open.setIcon(icon)
        self.action_open.setObjectName("action_open")
        self.action_save = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/rec/resources/save_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_save.setIcon(icon1)
        self.action_save.setObjectName("action_save")
        self.action_save_all = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/rec/resources/save_all_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_save_all.setIcon(icon2)
        self.action_save_all.setObjectName("action_save_all")
        self.action_new = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/rec/resources/new_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_new.setIcon(icon3)
        self.action_new.setObjectName("action_new")
        self.actiontest = QtWidgets.QAction(MainWindow)
        self.actiontest.setObjectName("actiontest")
        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        self.menufile.addAction(self.action_open)
        self.menufile.addSeparator()
        self.menufile.addAction(self.LastForms.menuAction())
        self.menufile.addSeparator()
        self.menufile.addAction(self.action_save)
        self.menufile.addAction(self.action_save_all)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.DrawButton.setText(_translate("MainWindow", "????????????????????"))
        self.ReflectButton.setText(_translate("MainWindow", "????????????????"))
        self.RotateButton.setText(_translate("MainWindow", "??????????????????"))
        self.ColorButton.setText(_translate("MainWindow", "???????????????? ??????????"))
        self.AlphaButton.setText(_translate("MainWindow", "????????????????????????"))
        self.BlurButton.setText(_translate("MainWindow", "??????????????"))
        self.SizeButton.setText(_translate("MainWindow", "????????????"))
        self.QuantizeButton.setText(_translate("MainWindow", "????????????????????"))
        self.label.setText(_translate("MainWindow", "Fill:"))
        self.label_2.setText(_translate("MainWindow", "Outline:"))
        self.menufile.setTitle(_translate("MainWindow", "File"))
        self.LastForms.setTitle(_translate("MainWindow", "?????????????????? ??????????"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.action_open.setText(_translate("MainWindow", "??????????????"))
        self.action_save.setText(_translate("MainWindow", "??????????????????"))
        self.action_save_all.setText(_translate("MainWindow", "?????????????????? ??????"))
        self.action_new.setText(_translate("MainWindow", "??????????????"))
        self.actiontest.setText(_translate("MainWindow", "test"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.actionRedo.setText(_translate("MainWindow", "Redo"))
        self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Shift+Z"))
