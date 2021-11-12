from declarations import *
from PyQt5.QtWidgets import QApplication


def main(argc: int, argv: List[str]):
    """starts the program"""
    from windows import MainWindow
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.excepthook = except_hook
    window.show()
    return sys.exit(app.exec())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
