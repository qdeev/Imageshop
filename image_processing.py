from PIL import ImageFilter

from constants import *
import PIL.Image
import PIL.ImageDraw
import PIL.ImageOps
from PyQt5.QtGui import QColor as Color


def convert_color(color: Color) -> Tuple[int, int, int, int]:
    return color.red(), color.green(), color.blue(), color.alpha()


class Image:

    def __setitem__(self, x: int, y: int, value: Color):
        self.__pixels_copy[x, y] = convert_color(value)

    def __getitem__(self, x: int, y: int) -> Tuple[int, int, int, int]:
        return self.__pixels_copy[x, y]

    def __init__(self, width: int, height: int, *args, filename=None, image=None):
        self.__filename = filename or 'temp'
        self.width = width
        self.height = height
        self.image = image or PIL.Image.new(mode="RGBA", size=(self.width, self.height), color=COLOR_WHITE)
        self.__pixels = self.image.load()

        self.__image_copy = self.image.copy()
        self.__pixels_copy = self.__image_copy.load()

        self.__pixels = self.image.load()
        self.__draw = PIL.ImageDraw.Draw(self.image)

    @classmethod
    def from_filename(cls, filename: str):
        image = PIL.Image.open(filename)
        width, height = image.size
        return cls(width, height, filename=filename, image=image)

    @property
    def filename(self) -> str:
        return self.__filename

    def draw_line(self, x0: int, y0: int, x1: int, y1: int, *args,
                  width: int = 1,
                  fill: Color = Color(*COLOR_BLACK)):
        self.__draw.line(x0, y0, x1, y1, fill=convert_color(fill), width=width)

    def draw_ellipse(self, x0: int, y0: int, x1: int, y1: int, *args,
                     width: int = 1,
                     fill: Color = Color(*COLOR_WHITE),
                     outline: Color = Color(*COLOR_BLACK)):
        self.__draw.ellipse(x0, y0, x1, y1, fill=convert_color(fill), width=width, outline=outline)

    def draw_square(self, x0: int, y0: int, x1: int, y1: int, *args,
                    width: int = 1,
                    fill: Color = Color(*COLOR_WHITE),
                    outline: Color = Color(*COLOR_BLACK)):
        self.__draw.rectangle(x0, y0, x1, y1, fill=convert_color(fill), width=width, outline=outline)

    def draw_polygon(self, *coords: List[Tuple[int]],
                     fill: Color = Color(*COLOR_WHITE),
                     outline: Color = Color(*COLOR_BLACK)):
        self.__draw.polygon(coords, fill=convert_color(fill), outline=outline)

    def rotate_left(self):
        self.image = self.image.rotate(90)

    def rotate_right(self):
        self.image = self.image.rotate(-90)

    def resize_image(self, size: Tuple[int]):
        self.image.resize(size)

    def quantize_image(self, number_of_colors: int):
        self.image.quantize(number_of_colors)

    def blur_image(self, radius: int = 2):
        self.image.filter(ImageFilter.GaussianBlur(radius=radius))

    def vertical_reflection(self):
        for x in range(self.width // 2):
            for y in range(self.height):
                self.__pixels[x, y], self.__pixels[self.width - x - 1, y] = \
                    self.__pixels[self.width - x - 1, y], self.__pixels[x, y]

    def horizontal_reflection(self):
        PIL.ImageOps.flip(self.image)

    def diagonal_reflection(self):
        for i in range(self.width):
            for j in range(self.width - i):
                self.__pixels[j, i], self.__pixels[self.width - i - 1, self.width - j - 1] = \
                    self.__pixels[self.width - i - 1, self.width - j - 1], self.__pixels[j, i]

    def change_alpha(self, alpha_value):
        self.image.putalpha(int(255 - alpha_value / 100 * 255))

    def only_red(self):
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.__pixels[i, j]
                self.__pixels_copy[i, j] = r, 0, 0

    def only_green(self):
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.__pixels[i, j]
                self.__pixels_copy[i, j] = 0, g, 0

    def only_blue(self):
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.__pixels[i, j]
                self.__pixels_copy[i, j] = 0, 0, b

    def to_default_color(self):
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.__pixels[i, j]
                self.__pixels_copy[i, j] = r, g, b

    def save(self, filename: str = ''):
        if filename.strip() != '':
            filename = filename
        else:
            filename = self.filename
        self.image.save(filename)
