from PyQt5.QtGui import QColor

from database import *
from declarations import *

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QDialog, QInputDialog, QMessageBox, QColorDialog
from PyQt5.QtWidgets import QFileDialog

from image_processing import Image
from widgets import TabsW, CanvasW


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('ui', 'ui_files', 'MainWindow.ui'), self)

        self.tabs_w = TabsW(self)
        self.canvasLayout.addWidget(self.tabs_w)

        self.draw_window = DrawWindow(parent=self)
        self.draw_window.hide()
        self.color_window = ColorWindow(parent=self)
        self.color_window.hide()
        self.rotate_window = RotateWindow(parent=self)
        self.rotate_window.hide()
        self.reflect_window = ReflectWindow(parent=self)
        self.reflect_window.hide()
        self.alpha_window = AlphaWindow(parent=self)
        self.alpha_window.hide()

        with Database() as database:
            f_names = database.cursor.execute("""SELECT DISTINCT filename FROM MetaData
                                ORDER BY creation_date DESC LIMIT 3""").fetchall()
            for f_name in f_names:
                self.LastForms.addAction(f_name[0])

        if not self.LastForms.isEmpty():
            for action in self.LastForms.actions():
                action.triggered.connect(self.open_recent)

        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.action_save.triggered.connect(self.save_an_image)
        self.action_open.triggered.connect(self.open_an_image)
        self.DrawButton.clicked.connect(self.draw_on_image)
        self.ReflectButton.clicked.connect(self.reflect_an_image)
        self.AlphaButton.clicked.connect(self.change_alpha)
        self.ColorButton.clicked.connect(self.change_color)
        self.BlurButton.clicked.connect(self.blur_an_image)
        self.SizeButton.clicked.connect(self.change_size)
        self.RotateButton.clicked.connect(self.rotate_image)
        self.QuantizeButton.clicked.connect(self.quantize_an_image)

        self.MainColor.setStyleSheet("background-color: {}".format(QColor(*COLOR_BLACK).name()))
        self.SecondaryColor.setStyleSheet("background-color: {}".format(QColor(*COLOR_WHITE).name()))

        self.MainColor.clicked.connect(self.choose_main_color)
        self.SecondaryColor.clicked.connect(self.choose_secondary_color)

    def closeEvent(self, event: QtGui.QCloseEvent):

        with Database() as database:
            database.cursor.execute("""DELETE FROM Images""")
            database.cursor.execute("""DELETE FROM TaskHistory""")
            database.cursor.execute(
                """DELETE FROM MetaData WHERE id NOT IN 
                (SELECT id FROM MetaData ORDER BY creation_date DESC LIMIT 3)""")
            database.commit()

        self.draw_window.destroy()
        self.color_window.destroy()
        self.rotate_window.destroy()
        self.reflect_window.destroy()
        self.alpha_window.destroy()
        event.accept()

    """rewriting the functions to connect them to the buttons on the main window"""

    def choose_main_color(self):
        fill_color = QColorDialog.getColor()
        if fill_color.isValid():
            self.MainColor.setStyleSheet("background-color: {}".format(fill_color.name()))
            self.tabs_w.fill_color = fill_color

    def choose_secondary_color(self):
        outline_color = QColorDialog.getColor()
        if outline_color.isValid():
            self.SecondaryColor.setStyleSheet("background-color: {}".format(outline_color.name()))
            self.tabs_w.outline_color = outline_color

    def draw_on_image(self):
        self.draw_window.show()

    def change_color(self):
        self.color_window.show()

    def rotate_image(self):
        self.rotate_window.show()

    def reflect_an_image(self):
        self.reflect_window.show()

    def change_alpha(self):
        self.alpha_window.show()

    def change_size(self):
        dialog = SizeDialog(parent=self)
        dialog.exec()

    def quantize_an_image(self):
        try:
            if self.tabs_w.get_canvas(self.tabs_w.currentIndex()).image.filename.split('.')[-1] == \
                    'png':
                coef, ok_pressed = QInputDialog.getInt(self, "Введите коеффициент",
                                                       "Коеффициент квантирования", 256, 1)
                self.tabs_w.get_canvas(self.tabs_w.currentIndex()).image.quantize_image(coef)
            else:
                MainWindow.show_ExceptDialog()
        except KeyError:
            MainWindow.show_ExceptDialog()

    @staticmethod
    def show_ExceptDialog():
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Требуется png изображение")
        msgBox.setWindowTitle("Alert")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    @staticmethod
    def show_ExceptDialog_no_image():
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Требуется изображение")
        msgBox.setWindowTitle("Alert")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def blur_an_image(self):
        try:
            coef, ok_pressed = QInputDialog.getInt(self, "Введите коеффициент",
                                                   "Коеффициент размытия")
            if ok_pressed:
                self.tabs_w.get_canvas(self.tabs_w.currentIndex()).image.blur_image(coef)
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()

    def add_new_canvas(self, width: int, height: int):
        self.tabs_w.addTab(CanvasW(Image(width, height)))

    def open_an_image(self):
        fname, ok_pressed = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')
        if ok_pressed:
            self.tabs_w.addTab(CanvasW(Image.from_filename(fname, callback=CanvasW.callback)))

    def open_recent(self):
        fname = self.sender().text()
        self.tabs_w.addTab(CanvasW(Image.from_filename(fname, callback=CanvasW.callback), True))

    def save_an_image(self):
        image_to_save = self.tabs_w.get_canvas(self.tabs_w.currentIndex()).image
        image_to_save.save()

    def undo(self):
        self.tabs_w.get_canvas(self.tabs_w.currentIndex()).undo()

    def redo(self):
        self.tabs_w.get_canvas(self.tabs_w.currentIndex()).redo()

    def save_all(self):
        for canvas in self.tabs_w.tabs_canvases:
            im_to_save = canvas.image
            im_to_save.save()

    """callback that lets to connect the windows below
       to the functions above"""


class DrawWindow(QMainWindow):
    def __init__(self, *args, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('ui', 'ui_files', 'DrawWindow.ui'), self)

        self.LineButton.clicked.connect(self.draw_line_window)
        self.SquareButton.clicked.connect(self.draw_square_window)
        self.CircleButton.clicked.connect(self.draw_ellipse_window)
        self.PolygonButton.clicked.connect(self.draw_polygon_window)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.hide()
        event.ignore()

    def draw_line_window(self):
        self.parent().tabs_w.shape = "line"

    def draw_square_window(self):
        self.parent().tabs_w.shape = "square"

    def draw_ellipse_window(self):
        self.parent().tabs_w.shape = "ellipse"

    def draw_polygon_window(self):
        self.parent().tabs_w.shape = "polygon"


class ReflectWindow(QMainWindow):
    def __init__(self, *args, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('ui', 'ui_files', 'ReflectWindow.ui'), self)

        self.VerticalButton.clicked.connect(self.vertical_reflection_window)
        self.HorizontalButton.clicked.connect(self.horizontal_reflection_window)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.hide()
        event.ignore()

    def vertical_reflection_window(self):
        try:
            self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.vertical_reflection()
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()

    def horizontal_reflection_window(self):
        try:
            self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.horizontal_reflection()
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()


class AlphaWindow(QMainWindow):
    def __init__(self, *args, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('ui', 'ui_files', 'AlphaWindow.ui'), self)

        self.AlphaSlider.valueChanged.connect(self.change_alpha_window)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.hide()
        event.ignore()

    def change_alpha_window(self):
        try:
            if self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.filename.split('.')[-1] == \
                    'png':
                self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.change_alpha(
                    self.AlphaSlider.value())
            else:
                MainWindow.show_ExceptDialog()
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()


class ColorWindow(QMainWindow):
    def __init__(self, *args, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('ui', 'ui_files', 'ColorWindow.ui'), self)

        self.RedButton.clicked.connect(self.only_red_window)
        self.GreenButton.clicked.connect(self.only_green_window)
        self.BlueButton.clicked.connect(self.only_blue_window)
        self.AllButton.clicked.connect(self.to_default_color_window)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.hide()
        event.ignore()

    def only_red_window(self):
        try:
            try:
                if self.parent().tabs_w.get_canvas(
                        self.parent().tabs_w.currentIndex()).image.filename.split('.')[-1] == 'jpg':
                    self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.only_red_jpg()
                elif self.parent().tabs_w.get_canvas(
                        self.parent().tabs_w.currentIndex()).image.filename.split('.')[-1] == 'png':
                    self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.only_red_png()
                else:
                    self.show_ExceptDialog_format()
            except TypeError:
                self.show_ExeptDialog_unable()
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()

    def only_green_window(self):
        try:
            try:
                if self.parent().tabs_w.get_canvas(
                        self.parent().tabs_w.currentIndex()).image.filename.split('.')[-1] == 'jpg':
                    self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.only_green_jpg()
                elif self.parent().tabs_w.get_canvas(
                        self.parent().tabs_w.currentIndex()).image.filename.split('.')[-1] == 'png':
                    self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.only_green_png()
                else:
                    self.show_ExceptDialog_format()
            except TypeError:
                self.show_ExeptDialog_unable()
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()

    def only_blue_window(self):
        try:
            try:
                if self.parent().tabs_w.get_canvas(
                        self.parent().tabs_w.currentIndex()).image.filename.split('.')[-1] == 'jpg':
                    self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.only_blue_jpg()
                elif self.parent().tabs_w.get_canvas(
                        self.parent().tabs_w.currentIndex()).image.filename.split('.')[-1] == 'png':
                    self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.only_blue_png()
                else:
                    self.show_ExceptDialog_format()
            except TypeError:
                self.show_ExeptDialog_unable()
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()

    def to_default_color_window(self):
        try:
            try:
                if self.parent().tabs_w.get_canvas(
                        self.parent().tabs_w.currentIndex()).image.filename.split('.')[-1] == 'jpg':
                    self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.to_default_color_jpg()
                elif self.parent().tabs_w.get_canvas(
                        self.parent().tabs_w.currentIndex()).image.filename.split('.')[-1] == 'png':
                    self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.to_default_color_png()
                else:
                    self.show_ExceptDialog_format()
            except TypeError:
                self.show_ExeptDialog_unable()
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()

    def show_ExceptDialog_format(self):
        """exception dialog that is shown when the wrong image resolution is given"""
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Неверный формат изображения")
        msgBox.setWindowTitle("Alert")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
        self.destroy()

    def show_ExeptDialog_unable(self):
        """exception dialog that is shown when
           it is impossible to change the color channel of the image"""
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Невозможно изменить изображение")
        msgBox.setWindowTitle("Alert")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()
        self.destroy()


class SizeDialog(QDialog):
    def __init__(self, *args, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('ui', 'ui_files', 'SizeDialog.ui'), self)

        self.pushButton.clicked.connect(self.commit)

    def commit(self):
        try:
            new_width = self.WspinBox.value()
            new_height = self.HspinBox.value()
            size = (new_width, new_height)
            self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.resize_image(size)
            self.accept()
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()


class RotateWindow(QMainWindow):
    def __init__(self, *args, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        uic.loadUi(os.path.join('ui', 'ui_files', 'RotateWidow.ui'), self)

        self.RightButton.clicked.connect(self.rotate_right_window)
        self.LeftButton.clicked.connect(self.rotate_left_window)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.hide()
        event.ignore()

    def rotate_right_window(self):
        try:
            self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.rotate_right()
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()

    def rotate_left_window(self):
        try:
            self.parent().tabs_w.get_canvas(self.parent().tabs_w.currentIndex()).image.rotate_left()
        except KeyError:
            MainWindow.show_ExceptDialog_no_image()
