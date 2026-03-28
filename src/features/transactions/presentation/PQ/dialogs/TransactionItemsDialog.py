from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from src.features.transactions.application.interfaces.ITransactionItemsDialog import (
    ITransactionItemsDialog,
)
from src.features.transactions.application.value_objects.TransactionItem import (
    TransactionItem,
)
from src.shared.application.dtos.ObjectDisplayDTO import ObjectDisplayDTO
from src.shared.application.Interfaces.IABCWidget import IABCDialog


class TransactionItemsDialog(ITransactionItemsDialog, IABCDialog):
    """Диалог для добавления нескольких товаров в транзакцию (только UI)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

        self.PRODUCT_ID_ROLE = Qt.UserRole + 1
        self.PRODUCT_NAME_ROLE = Qt.UserRole + 2

    def init_ui(self):
        self.setWindowTitle("Добавить товары в операцию")
        self.setGeometry(150, 150, 600, 500)

        layout = QVBoxLayout()

        # Список доступных товаров
        layout.addWidget(QLabel("Доступные товары:"))
        self.products_list = QListWidget()
        layout.addWidget(self.products_list)

        # Количество
        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel("Количество:"))
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(9999)
        self.quantity_input.setValue(1)
        quantity_layout.addWidget(self.quantity_input)
        quantity_layout.addStretch()
        layout.addLayout(quantity_layout)

        # Кнопка добавления
        self.add_button = QPushButton("Добавить в операцию")
        layout.addWidget(self.add_button)

        # Список выбранных товаров
        layout.addWidget(QLabel("Выбранные товары:"))
        self.selected_table = QTableWidget()
        self.selected_table.setColumnCount(3)
        self.selected_table.setHorizontalHeaderLabels(
            ["Товар", "Количество", "Действие"]
        )
        self.selected_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.selected_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.selected_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        layout.addWidget(self.selected_table)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.confirm_btn = QPushButton("Подтвердить выбор")

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.confirm_btn)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def set_on_items_confirmed(self, callback):
        self.confirm_btn.clicked.connect(callback)

    def set_on_add_item_requested(self, callback):
        def on_add():
            current = self.products_list.currentItem()
            if not current:
                QMessageBox.warning(self, "Ошибка", "Выберите товар из списка!")
                return

            id = current.data(self.PRODUCT_ID_ROLE)
            name = current.data(self.PRODUCT_NAME_ROLE)

            data = {
                "product_id": id,
                "quantity": self.quantity_input.value(),
                "name": name,
            }
            callback(data)

        self.add_button.clicked.connect(on_add)

    def set_on_remove_item_requested(self, callback):
        """Устанавливает колбэк для удаления товара"""
        self._on_remove_callback = callback

    def set_products(self, products: List[ObjectDisplayDTO]):
        """Заполняет список доступных товаров"""
        self.products_list.clear()
        for product in products:
            item = QListWidgetItem(product.object_name)
            item.setData(self.PRODUCT_ID_ROLE, product.object_id)
            item.setData(self.PRODUCT_NAME_ROLE, product.object_name)
            self.products_list.addItem(item)

    def update_table(self, items: List[TransactionItem]):
        """Обновляет таблицу выбранных товаров"""
        self.selected_table.setRowCount(len(items))

        for row, item in enumerate(items):
            name_item = QTableWidgetItem(item.product_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.selected_table.setItem(row, 0, name_item)

            qty_item = QTableWidgetItem(str(item.quantity))
            qty_item.setFlags(qty_item.flags() & ~Qt.ItemIsEditable)
            self.selected_table.setItem(row, 1, qty_item)

            delete_btn = QPushButton("Удалить")

            delete_btn.clicked.connect(
                lambda checked, r=row: self._on_remove_clicked(r)
            )
            self.selected_table.setCellWidget(row, 2, delete_btn)

    def _on_remove_clicked(self, row):
        """Внутренний обработчик удаления — вызывает колбэк из презентера"""
        if hasattr(self, "_on_remove_callback") and self._on_remove_callback:
            self._on_remove_callback(row)

    def close_dialog(self):
        self.accept()
