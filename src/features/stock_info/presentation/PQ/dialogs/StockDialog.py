from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from src.features.stock_info.application.interfaces.IStockDialog import IStockDialog
from src.shared.application.Interfaces.IABCWidget import IABCDialog


class StockDialog(IStockDialog, IABCDialog):
    """Диалог для просмотра остатков на складах (только UI)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Товары на складе")
        self.setGeometry(100, 100, 800, 500)

        layout = QVBoxLayout()

        # Выбор филиала и склада
        selection_layout = QHBoxLayout()

        selection_layout.addWidget(QLabel("Филиал:"))
        self.branch_combo = QComboBox()
        selection_layout.addWidget(self.branch_combo)

        selection_layout.addWidget(QLabel("Склад:"))
        self.warehouse_combo = QComboBox()
        selection_layout.addWidget(self.warehouse_combo)

        self.load_btn = QPushButton("Загрузить остатки")
        selection_layout.addWidget(self.load_btn)

        selection_layout.addStretch()
        layout.addLayout(selection_layout)

        # Таблица остатков
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(3)
        self.stock_table.setHorizontalHeaderLabels(["Товар", "Остаток", "Стоимость"])
        self.stock_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.stock_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.stock_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )

        layout.addWidget(self.stock_table)

        # Итоги
        self.summary_label = QLabel("Выберите филиал и склад")
        layout.addWidget(self.summary_label)

        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close_dialog)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def set_on_branch_changed(self, callback):
        def on_changed():
            branch_id = self.branch_combo.currentData()
            callback(branch_id)

        self.branch_combo.currentIndexChanged.connect(on_changed)

    def set_on_load_stock_requested(self, callback):
        def on_load():
            params = {
                "branch_id": self.branch_combo.currentData(),
                "warehouse_id": self.warehouse_combo.currentData(),
            }
            callback(params)

        self.load_btn.clicked.connect(on_load)

    # Методы для внешнего управления
    def set_branches(self, branches, has_branches):
        """Заполняет список филиалов"""
        self.branch_combo.clear()

        if has_branches:
            for branch in branches:
                self.branch_combo.addItem(branch.name, branch.local_id)
        else:
            self.branch_combo.addItem("Филиалов нету!", "")

    def set_warehouses(self, warehouses):
        """Заполняет список складов"""
        self.warehouse_combo.clear()

        for wh in warehouses:
            self.warehouse_combo.addItem(wh.object_name, wh.object_id)

    def display_stock(self, items, total_value):
        if items:
            self.stock_table.setRowCount(len(items.data))
            for row, item in enumerate(items.data):
                self.stock_table.setItem(row, 0, QTableWidgetItem(item.product_name))
                self.stock_table.setItem(row, 1, QTableWidgetItem(str(item.quantity)))
                self.stock_table.setItem(row, 2, QTableWidgetItem(f"{item.cost:.2f} ₽"))

            self.summary_label.setText(
                f"Товаров: {len(items.data)} | Общая стоимость: {total_value:.2f} ₽"
            )
        else:
            self.stock_table.setRowCount(0)
            self.summary_label.setText("")

    def close_dialog(self):
        self.accept()
