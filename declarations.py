import os
import sys
from typing import *
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG,
                    filename="log.txt", filemode='a')

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 820
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
DATABASE_NAME = 'db.sqlite'
