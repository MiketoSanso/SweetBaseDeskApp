from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from src.features.transactions.application.interfaces.ITransactionTab import (
    ITransactionTab,
)
from src.features.transactions.application.value_objects.TransactionItem import (
    TransactionItem,
)
from src.shared.application.Interfaces.IABCWidget import IABCWidget


class TransactionTab(ITransactionTab, IABCWidget):
    """Вкладка прихода/ухода товаров (только UI)"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout()

        title = QLabel("Учет прихода и ухода товаров")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Группа выбора операции
        operation_group = QGroupBox("Операция")
        operation_layout = QVBoxLayout()

        # Тип операции
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Тип операции:"))
        self.trans_type_combo = QComboBox()
        self.trans_type_combo.addItems(["Приход", "Уход"])
        type_layout.addWidget(self.trans_type_combo)
        type_layout.addStretch()
        operation_layout.addLayout(type_layout)

        # Выбор филиала
        branch_layout = QHBoxLayout()
        branch_layout.addWidget(QLabel("Филиал:"))
        self.trans_branch_combo = QComboBox()
        branch_layout.addWidget(self.trans_branch_combo)
        branch_layout.addStretch()
        operation_layout.addLayout(branch_layout)

        # Выбор склада
        warehouse_layout = QHBoxLayout()
        warehouse_layout.addWidget(QLabel("Склад:"))
        self.trans_warehouse_combo = QComboBox()
        warehouse_layout.addWidget(self.trans_warehouse_combo)
        warehouse_layout.addStretch()
        operation_layout.addLayout(warehouse_layout)

        # Примечание
        note_layout = QHBoxLayout()
        note_layout.addWidget(QLabel("Примечание:"))
        self.trans_note = QLineEdit()
        self.trans_note.setPlaceholderText("Примечание к операции")
        note_layout.addWidget(self.trans_note)
        operation_layout.addLayout(note_layout)

        operation_group.setLayout(operation_layout)
        layout.addWidget(operation_group)

        # Группа товаров
        products_group = QGroupBox("Товары в операции")
        products_layout = QVBoxLayout()

        # Кнопка добавления товаров
        self.add_items_btn = QPushButton("+ Добавить товары")
        products_layout.addWidget(self.add_items_btn)

        # Таблица выбранных товаров
        self.trans_items_table = QTableWidget()
        self.trans_items_table.setColumnCount(2)
        self.trans_items_table.setHorizontalHeaderLabels(["Товар", "Количество"])
        self.trans_items_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.trans_items_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.trans_items_table.setMaximumHeight(200)
        products_layout.addWidget(self.trans_items_table)

        # Итоговая информация
        self.trans_summary_label = QLabel("Товаров в операции: 0")
        products_layout.addWidget(self.trans_summary_label)

        products_group.setLayout(products_layout)
        layout.addWidget(products_group)

        # Кнопка подтверждения
        self.confirm_trans_btn = QPushButton("Подтвердить операцию")
        layout.addWidget(self.confirm_trans_btn)

        layout.addStretch()
        self.setLayout(layout)

    def set_on_add_items_requested(self, callback):
        self.add_items_btn.clicked.connect(callback)

    def set_on_process_transaction_requested(self, callback):
        def _on_process_transaction_requested():
            is_arrival = self.trans_type_combo.currentIndex() == 0

            data = {
                "is_arrival": is_arrival,
                "branch_id": self.trans_branch_combo.currentData(),
                "warehouse_id": self.trans_warehouse_combo.currentData(),
                "note": self.trans_note.text().strip(),
            }
            callback(data)

        self.confirm_trans_btn.clicked.connect(_on_process_transaction_requested)

    def set_on_change_branch_requested(self, callback):
        def on_change_branch_requested():
            id = self.trans_branch_combo.currentData() or 1
            callback(id)

        self.trans_branch_combo.currentIndexChanged.connect(on_change_branch_requested)

    def set_branches(self, branches, has_branches):
        """Заполняет список филиалов"""
        self.trans_branch_combo.clear()
        if has_branches:
            for branch in branches:
                self.trans_branch_combo.addItem(branch.name, branch.local_id)
        else:
            self.trans_branch_combo.addItem("Нет филиалов", None)

    def set_warehouses(self, warehouses):
        """Заполняет список складов"""
        self.trans_warehouse_combo.clear()
        if warehouses:
            for warehouse in warehouses:
                self.trans_warehouse_combo.addItem(
                    warehouse.object_name, warehouse.object_id
                )
        else:
            self.trans_warehouse_combo.addItem("Нет складов", None)

    def update_display(self, items: List[TransactionItem]):
        """Обновляет таблицу товаров"""
        self.trans_items_table.setRowCount(len(items))

        for row, item in enumerate(items):
            name_item = QTableWidgetItem(item.product_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.trans_items_table.setItem(row, 0, name_item)

            qty_item = QTableWidgetItem(str(item.quantity))
            qty_item.setFlags(qty_item.flags() & ~Qt.ItemIsEditable)
            self.trans_items_table.setItem(row, 1, qty_item)

        total_items = len(items)
        total_qty = sum(item.quantity for item in items)
        self.trans_summary_label.setText(
            f"Товаров в операции: {total_items} | Общее количество: {total_qty}"
        )
