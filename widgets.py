from PyQt5.QtGui import QPixmap

from constants import *

from PyQt5.QtWidgets import QTabWidget, QLabel, QWidget
from image_processing import Image


class CanvasW(QLabel):

    def __init__(self, image: Image, *args, parent=None):
        super().__init__(parent)
        self.image = image
        self.pixmap_: QPixmap = QPixmap(self.image.filename)
        self.setPixmap(self.pixmap_)


class TabsW(QTabWidget):

    def __init__(self, *args, parent=None):
        super().__init__(parent)

        self.tabs_canvases: List[CanvasW] = []

    def addTab(self, canvas: CanvasW, **kwargs) -> int:
        self.tabs_canvases.append(canvas)
        filename = canvas.image.filename.split("/")[-1]
        return super().addTab(canvas, filename)
