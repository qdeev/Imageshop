import os.path

from constants import *

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog

from image_processing import Image
from widgets import TabsW, CanvasW


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('ui', 'ui_files', 'main_window.ui'), self)

        self.tabs_w = TabsW()
        self.canvasLayout.addWidget(self.tabs_w)

        self.action_save.triggered.connect(self.save_an_image)
        self.action_open.triggered.connect(self.open_an_image)
        self.action_new.triggered.connect(self.create_an_image)

    def create_an_image(self):
        dialog = DialogWH(parent=self, callback=MainWindow.callback)
        dialog.exec()

    def add_new_canvas(self, width: int, height: int):
        self.tabs_w.addTab(CanvasW(Image(width, height)))

    def open_an_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.tabs_w.addTab(CanvasW(Image.from_filename(fname)))

    def save_an_image(self):
        image_to_save = self.tabs_w.tabs_canvases[self.tabs_w.currentIndex()].image
        image_to_save.save()

    def save_all(self):
        for canvas in self.tabs_w.tabs_canvases:
            im_to_save = canvas.image
            im_to_save.save()

    @staticmethod
    def callback(self, *args, reason: str = '', **kwargs):
        if reason == 'failed':
            return
        elif reason == 'DialogWH':
            self.add_new_canvas(kwargs['width'], kwargs['height'])


class DialogWH(QDialog):
    def __init__(self, *args, parent=None, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('ui', 'ui_files', 'dialog_wh.ui'), self)

        self.pushButton.clicked.connect(self.commit)

    def closeEvent(self, event):
        self.callback(self.parentWidget(), reason='failed')
        self.reject()

    def commit(self):
        self.callback(self.parentWidget(), reason='DialogWH',
                      width=self.spinBox.value(), height=self.spinBox_2.value())
        self.accept()
