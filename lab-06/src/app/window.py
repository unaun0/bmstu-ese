from PyQt5.QtWidgets import (
    QMainWindow,
    QToolBar,
    QMessageBox
)
from PyQt5.QtWidgets import QAction
from dataclasses import dataclass

from app.page import Page


@dataclass
class Settings:
    title = 'Модель COCOMO'
    width = 1450
    height = 700

    info_title = 'О программе'
    info_text = 'Лабораторная работа выполнена Цховребовой Я. Р., ИУ7-84Б'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(Settings.title)
        self.setFixedSize(Settings.width, Settings.height)

        self.__createToolbar()
        page = Page()
        self.setCentralWidget(page)

    def __createToolbar(self):
        toolbar = QToolBar()

        info_button = QAction(Settings.info_title, self)
        info_button.triggered.connect(self.__get_info)
        info_button.setCheckable(True)
        toolbar.addAction(info_button)

        self.addToolBar(toolbar)

    def __get_info(self):
        info = QMessageBox()

        info.setText(Settings.info_text)
        info.setWindowTitle(Settings.info_title)

        info.exec()