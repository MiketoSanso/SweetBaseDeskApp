import sys

from PySide6.QtWidgets import QApplication, QStyleFactory


class Window:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.app.setStyle(QStyleFactory.create("Fusion"))

        self.app.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f5f5;
                }
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
                QListWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 5px;
                }
                QLabel {
                    color: #333;
                    padding: 5px;
                }
                QTabWidget::pane {
                    border: 1px solid #ddd;
                    background-color: white;
                    border-radius: 4px;
                }
                QTabBar::tab {
                    background-color: #e0e0e0;
                    padding: 8px 16px;
                    margin-right: 2px;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background-color: white;
                    font-weight: bold;
                    border-bottom: 2px solid #2196F3;
                }
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
                QTableWidget {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    gridline-color: #eee;
                }
                QTableWidget::item {
                    padding: 5px;
                }
                QHeaderView::section {
                    background-color: #f0f0f0;
                    padding: 5px;
                    border: 1px solid #ddd;
                    font-weight: bold;
                }
                QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                    padding: 5px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    background-color: white;
                }
                QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                    border: 1px solid #2196F3;
                }
            """)

    def exit(self):
        sys.exit(self.app.exec())
