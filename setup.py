import sys
from cx_Freeze import setup, Executable

application_title = "YandexProject1"
main_python_file = "main.py"
base = None
if sys.platform == "win32":
    base = "Win32GUI"

packages = ["PyQt5.QtGui", "PyQt5.QtWidgets", "PyQt5.QtCore", "PyQt5", "io", "sys", "PIL.Image", "PIL.ImageDraw",
            "PIL.ImageOps", "PIL", "datetime", "os", "typing", "logging", "sqlite3"]

setup(
    name=application_title,
    version="0.1",
    description="YandexProject1",
    options={"build_exe": {"packages": packages}},
    executables=[Executable(main_python_file, base=base, icon='ui/resources/main_icon.ico')])
