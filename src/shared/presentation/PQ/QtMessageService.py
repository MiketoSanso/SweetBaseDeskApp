from PySide6.QtWidgets import QMessageBox, QWidget

from src.shared.application.Interfaces.IMessageService import IMessageService


class QtMessageService(IMessageService):
    def show_success(self, title: str, message: str, parent_widget: QWidget = None):
        QMessageBox.information(parent_widget, title, message)

    def show_error(self, title: str, message: str, parent_widget: QWidget = None):
        QMessageBox.critical(parent_widget, title, message)

    def show_question(
        self, title: str, message: str, parent_widget: QWidget = None
    ) -> bool:
        result = QMessageBox.question(parent_widget, title, message)
        return result == QMessageBox.Yes
