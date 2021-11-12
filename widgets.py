import datetime

from declarations import *
from database import *

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QTabWidget, QLabel
from image_processing import Image, image_to_bytes, image_from_bytes


class CanvasW(QLabel):

    def __init__(self, image: Image, is_recent: bool = False, *args, parent=None):
        super().__init__(parent)
        self.image = image
        self.image.callback_arg = self
        self.pixmap_: QPixmap = QPixmap(self.image.filename)
        self.setPixmap(self.pixmap_)
        self.coords: List[Tuple[int, int]] = []

        with Database() as database:
            time = datetime.datetime.now()
            database.cursor.execute(f"""INSERT INTO Images(image) VALUES (?)""", (image_to_bytes(self.image),))
            self.id = database.cursor.execute("""SELECT id FROM Images ORDER BY id DESC LIMIT 1""").fetchone()[0]
            database.cursor.execute(
                """INSERT INTO TaskHistory(step, changed_image, image_id) VALUES (0, ?, ?)""",
                (image_to_bytes(self.image), self.id,))
            self.step = 0
            if is_recent:
                database.cursor.execute(f"""UPDATE MetaData
                                    SET image_id = {self.id},
                                    creation_date = '{time.timestamp()}'
                                    WHERE filename = '{self.image.filename}' """)
            else:
                database.cursor.execute(f"""INSERT INTO MetaData(filename, resolution, creation_date, image_id)
                                   VALUES (?, ?, ?, ?)""",
                                        (self.image.filename, "{0}x{1}".format(*self.image.image.size),
                                         time.timestamp(), self.id))
            database.commit()
        self.initUI()

    def initUI(self):
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    @staticmethod
    def callback(self):
        with Database() as database:
            self.step += 1
            if database.cursor.execute(
                    f"""SELECT step FROM TaskHistory 
                    WHERE image_id = {self.id} ORDER BY step DESC""").fetchone()[0] <= self.step:
                database.cursor.execute("""INSERT INTO TaskHistory (step, changed_image, image_id) VALUES (?, ?, ?)""",
                                        (self.step, image_to_bytes(self.image), self.id))
            else:
                database.cursor.execute(f"""UPDATE TaskHistory 
                                            SET changed_image = (?) 
                                            WHERE step = {self.step}""", (image_to_bytes(self.image),))
                database.cursor.execute(f"""DELETE FROM TaskHistory
                                            WHERE step > {self.step + 1}""")
            database.commit()
        self.pixmap_ = QPixmap(self.image.filename)
        self.setPixmap(self.pixmap_)

    def mousePressEvent(self, event):
        """remembers the coordinates of the cursor when the left button is pressed or
            creates and shows the polygon when the right button is clicked"""
        if event.button() == Qt.LeftButton:
            self.x0, self.y0 = event.x() - self.offset_x, event.y() - self.offset_y
            if self.parent().parent().shape == 'polygon' and not self.coords:
                self.coords.append((self.x0, self.y0))
        elif event.button() == Qt.RightButton:
            self.image.draw_polygon(tuple(self.coords), fill=self.parent().parent().fill_color,
                                    outline=self.parent().parent().outline_color)
            self.coords = []
            self.parent().parent().shape = ''

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:

        """connecting drawing functions to get coordinates"""
        if event.button() == Qt.LeftButton:
            if self.parent().parent().shape == 'line':
                self.image.draw_line(self.x0, self.y0, event.x() - self.offset_x, event.y() - self.offset_y,
                                     fill=self.parent().parent().fill_color)
                self.parent().parent().shape = ''

            elif self.parent().parent().shape == 'ellipse':
                self.image.draw_ellipse(self.x0, self.y0, event.x() - self.offset_x, event.y() - self.offset_y,
                                        fill=self.parent().parent().fill_color,
                                        outline=self.parent().parent().outline_color)
                self.parent().parent().shape = ''

            elif self.parent().parent().shape == 'square':
                self.image.draw_square(self.x0, self.y0, event.x() - self.offset_x, event.y() - self.offset_y,
                                       fill=self.parent().parent().fill_color,
                                       outline=self.parent().parent().outline_color)
                self.parent().parent().shape = ''

            elif self.parent().parent().shape == 'polygon':
                self.coords.append((event.x() - self.offset_x, event.y() - self.offset_y))

    def undo(self):
        if self.step >= 1:
            self.step -= 1
            with Database() as database:
                self.image.set_new_image(image_from_bytes(bytes(database.cursor.execute(
                    f"""SELECT changed_image FROM TaskHistory 
                    WHERE step = {self.step} AND image_id = {self.id}""").fetchone()[0])))
                self.image.save()

            self.pixmap_ = QPixmap(self.image.filename)
            self.setPixmap(self.pixmap_)

    def redo(self):
        with Database() as database:
            if database.cursor.execute(f"""SELECT step FROM TaskHistory 
                        WHERE image_id = {self.id} ORDER BY step DESC""").fetchone()[0] > self.step:
                self.step += 1
                self.image.set_new_image(image_from_bytes(bytes(database.cursor.execute(
                    f"""SELECT changed_image FROM TaskHistory 
                    WHERE step = {self.step} AND image_id = {self.id}""").fetchone()[0])))
                self.image.save()

                self.pixmap_ = QPixmap(self.image.filename)
                self.setPixmap(self.pixmap_)

    """counting the offset values to centralize the painting functions
       relatively the image but not the tab widget"""

    @property
    def offset_x(self):
        center = self.width() // 2 - self.image.width // 2
        return center

    @property
    def offset_y(self):
        center = self.height() // 2 - self.image.height // 2
        return center


class TabsW(QTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        """list of canvases which allows to ask the current tab widget id"""
        self.tabs_canvases: List[CanvasW] = []

        self.shape = ''
        self.fill_color = QColor(*COLOR_BLACK)
        self.outline_color = QColor(*COLOR_WHITE)

    def addTab(self, canvas: CanvasW, **kwargs) -> int:
        self.tabs_canvases.append(canvas)
        filename = canvas.image.filename.split("/")[-1]
        return super().addTab(self.tabs_canvases[-1], filename)

    def get_canvas(self, index: int):
        if index == -1:
            return CanvasW(Image(100, 100))
        return self.tabs_canvases[index]
