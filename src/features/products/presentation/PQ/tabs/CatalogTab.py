from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from src.features.products.application.interfaces.ICatalogTab import ICatalogTab
from src.shared.application.Interfaces.IABCWidget import IABCWidget


class CatalogTab(ICatalogTab, IABCWidget):
    """Вкладка каталога изделий (только UI)"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        layout = QVBoxLayout()

        # Заголовок и кнопки
        header_layout = QHBoxLayout()
        title = QLabel("Каталог изделий")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        self.add_product_btn = QPushButton("+ Новое изделие")

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.add_product_btn)
        layout.addLayout(header_layout)

        # Список изделий
        self.catalog_list = QListWidget()
        layout.addWidget(self.catalog_list)

        # Кнопка обновления
        self.refresh_btn = QPushButton("Обновить список")
        layout.addWidget(self.refresh_btn)

        self.setLayout(layout)

    def set_on_add_product_requested(self, callback):
        self.add_product_btn.clicked.connect(callback)

    def set_on_refresh_catalog_requested(self, callback):
        self.refresh_btn.clicked.connect(callback)

    def set_on_product_selected(self, callback):
        def _on_product_selected(item):
            callback(item.data(Qt.UserRole))

        self.catalog_list.itemDoubleClicked.connect(_on_product_selected)

    # Методы для внешнего управления UI
    def display_products(self, products, has_products):
        """Отображает список продуктов"""
        self.catalog_list.clear()

        if not has_products:
            item = QListWidgetItem("Нет изделий. Добавьте первое изделие!")
            item.setForeground(Qt.gray)
            self.catalog_list.addItem(item)
            return

        for product in products:
            item_text = (
                f"{product['name']} | Всего на складах: {product['stock_count']} шт."
            )
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, product["id"])
            self.catalog_list.addItem(item)
