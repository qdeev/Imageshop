from declarations import *
from io import BytesIO

import PIL.Image
import PIL.ImageDraw
import PIL.ImageOps
from PyQt5.QtGui import QColor as Color
from PIL import ImageFilter


def convert_color(color: Color) -> str:
    """converts the RGB color to hex color"""
    logging.info('Function "convert_color"')
    return '#{:02x}{:02x}{:02x}'.format(color.red(), color.green(), color.blue())


class Image:

    def __init__(self, width: int, height: int, *args, filename=None, image=None, callback=lambda self: None):
        self.__filename = filename or 'temp'

        self.image = image or PIL.Image.new(mode="RGBA", size=(width, height), color=COLOR_WHITE)
        self.__pixels = self.image.load()

        """used for changing the color channel"""
        self.__image_copy = self.image.copy()

        self.__pixels_base = self.__image_copy.load()

        self.__pixels = self.image.load()
        self.__draw = PIL.ImageDraw.Draw(self.image)

        self.callback = callback
        self.callback_arg = None

    @classmethod
    def from_filename(cls, filename: str, callback=lambda self: None):
        logging.info('Function "from_filename"')
        """classmethod that creates an Image object from given filename"""
        image = PIL.Image.open(filename)
        width, height = image.size
        return cls(width, height, filename=filename, image=image, callback=callback)

    """returning"""

    @property
    def width(self) -> int:
        return self.image.size[0]

    @property
    def height(self) -> int:
        return self.image.size[-1]

    @property
    def filename(self) -> str:
        return self.__filename

    """drawing"""

    def draw_line(self, x0: int, y0: int, x1: int, y1: int, *args,
                  width: int = 3,
                  fill: Color = Color(*COLOR_BLACK)):
        logging.info('Function "draw_line"')
        self.__draw.line([(x0, y0), (x1, y1)], fill=convert_color(fill), width=width)
        self.__image_copy = self.image.copy()
        self.__pixels_base = self.__image_copy.load()
        self.update()

    def draw_ellipse(self, x0: int, y0: int, x1: int, y1: int, *args,
                     width: int = 1,
                     fill: Color = Color(*COLOR_WHITE),
                     outline: Color = Color(*COLOR_BLACK)):
        logging.info('Function "draw_ellipse"')
        self.__draw.ellipse([(x0, y0), (x1, y1)], fill=convert_color(fill), width=width,
                            outline=convert_color(outline))
        self.__image_copy = self.image.copy()
        self.__pixels_base = self.__image_copy.load()
        self.update()

    def draw_square(self, x0: int, y0: int, x1: int, y1: int, *args,
                    width: int = 1,
                    fill: Color = Color(*COLOR_WHITE),
                    outline: Color = Color(*COLOR_BLACK)):
        logging.info('Function "draw_square"')
        self.__draw.rectangle([(x0, y0), (x1, y1)], fill=convert_color(fill), width=width,
                              outline=convert_color(outline))
        self.__image_copy = self.image.copy()
        self.__pixels_base = self.__image_copy.load()
        self.update()

    def draw_polygon(self, coords: Tuple[Tuple[int, int]],
                     fill: Color = Color(*COLOR_WHITE),
                     outline: Color = Color(*COLOR_BLACK)):
        logging.info('Function "draw_polygon"')
        self.__draw.polygon(coords, fill=convert_color(fill), outline=convert_color(outline))
        self.__image_copy = self.image.copy()
        self.__pixels_base = self.__image_copy.load()
        self.update()

    """rotating"""

    def rotate_left(self):
        logging.info('Function "rotate_left"')
        self.image = self.image.rotate(90, expand=True)
        self.__draw = PIL.ImageDraw.Draw(self.image)
        self.update()

    def rotate_right(self):
        logging.info('Function "rotate_right"')
        self.image = self.image.rotate(-90, expand=True)
        self.__draw = PIL.ImageDraw.Draw(self.image)
        self.update()

    """changing the size"""

    def resize_image(self, size: Tuple[int]):
        logging.info('Function "resize_image"')
        self.image = self.image.resize(size)
        self.__draw = PIL.ImageDraw.Draw(self.image)
        self.__image_copy = self.image.copy()
        self.__pixels_base = self.__image_copy.load()
        self.update()

    def quantize_image(self, number_of_colors: int):
        logging.info('Function "quantize_image"')
        """leaves a certain number of colors
            the more of the color in the picture the more priority it has"""
        self.image = self.image.quantize(number_of_colors).convert("RGBA")
        self.__draw = PIL.ImageDraw.Draw(self.image)
        self.update()

    def blur_image(self, radius: int = 2):
        logging.info('Function "blur_image"')
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius=radius))
        self.__pixels = self.image.load()
        self.__image_copy = self.image.copy()
        self.__pixels_base = self.__image_copy.load()
        self.__pixels = self.image.load()
        self.__draw = PIL.ImageDraw.Draw(self.image)
        self.update()

    """reflecting"""

    def vertical_reflection(self):
        logging.info('Function "vertical_reflection"')
        self.image = self.image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        self.__draw = PIL.ImageDraw.Draw(self.image)
        self.update()

    def horizontal_reflection(self):
        logging.info('Function "horizontal_reflection"')
        self.image = self.image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        self.__draw = PIL.ImageDraw.Draw(self.image)
        self.update()

    def change_alpha(self, alpha_value):
        logging.info('Function "change_alpha"')
        """changes the alpha value of the Image"""
        self.image.putalpha(int(255 - alpha_value / 100 * 255))
        self.update()

    """changing the color channel for jpg"""

    def only_red_jpg(self):
        logging.info('Function "only_red_jpg"')
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.__pixels_base[i, j]
                self.__pixels[i, j] = r, 0, 0
        self.update()

    def only_green_jpg(self):
        logging.info('Function "only_green_jpg"')
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.__pixels_base[i, j]
                self.__pixels[i, j] = 0, g, 0
        self.update()

    def only_blue_jpg(self):
        logging.info('Function "only_blue_jpg"')
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.__pixels_base[i, j]
                self.__pixels[i, j] = 0, 0, b
        self.update()

    def to_default_color_jpg(self):
        logging.info('Function "to_default_color_jpg"')
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.__pixels_base[i, j]
                self.__pixels[i, j] = r, g, b
        self.update()

    """changing the color channel for png"""

    def only_red_png(self):
        logging.info('Function "only_red_png"')
        for i in range(self.width):
            for j in range(self.height):
                r, g, b, a = self.__pixels_base[i, j]
                self.__pixels[i, j] = r, 0, 0, a
        self.update()

    def only_green_png(self):
        logging.info('Function "only_green_png"')
        for i in range(self.width):
            for j in range(self.height):
                r, g, b, a = self.__pixels_base[i, j]
                self.__pixels[i, j] = 0, g, 0, a
        self.update()

    def only_blue_png(self):
        logging.info('Function "only_blue_png"')
        for i in range(self.width):
            for j in range(self.height):
                r, g, b, a = self.__pixels_base[i, j]
                self.__pixels[i, j] = 0, 0, b, a
        self.update()

    def to_default_color_png(self):
        logging.info('Function "to_default_color_png"')
        for i in range(self.width):
            for j in range(self.height):
                r, g, b, a = self.__pixels_base[i, j]
                self.__pixels[i, j] = r, g, b, a
        self.update()

    def save(self, filename: str = ''):
        logging.info('Function "save"')
        if filename.strip() != '':
            filename = filename
        else:
            filename = self.filename
        self.image.save(filename)
        self.__pixels = self.image.load()

    def update(self):
        logging.info('Function "update"')
        self.save()
        self.callback(self.callback_arg)

    def set_new_image(self, image: PIL.Image):
        logging.info('Function "set_new_image"')
        self.image = image
        self.__pixels = self.image.load()
        self.__image_copy = self.image.copy()
        self.__pixels_base = self.__image_copy.load()
        self.__pixels = self.image.load()
        self.__draw = PIL.ImageDraw.Draw(self.image)


def image_to_bytes(image: Image) -> bytes:
    bytearr = BytesIO()
    format_ = image.filename.split('.')[-1].upper()
    image.image.save(bytearr, format_ if format_ != "JPG" else "JPEG")
    bytearr.seek(0)
    bytearr = bytearr.read()
    return bytearr


def image_from_bytes(bytearr: bytes) -> PIL.Image:
    logging.info('Function "from_bytes"')
    image = PIL.Image.open(BytesIO(bytearr))
    return image
