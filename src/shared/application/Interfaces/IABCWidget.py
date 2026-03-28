from abc import ABCMeta

from PySide6.QtWidgets import QDialog, QMainWindow, QWidget


class MetaQObjectABCMeta(type(QWidget), ABCMeta):
    pass


class IABCWidget(QWidget, metaclass=MetaQObjectABCMeta):
    pass


class IABCDialog(QDialog, metaclass=MetaQObjectABCMeta):
    pass


class IABCMainWindow(QMainWindow, metaclass=MetaQObjectABCMeta):
    pass
