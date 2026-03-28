from typing import List

from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from src.features.products.application.dtos.IngredientDisplayDTO import (
    IngredientDisplayDTO,
)
from src.features.products.application.dtos.StockItemDisplayDTO import (
    StockItemDisplayDTO,
)
from src.features.products.application.interfaces.IProductDetailsDialog import (
    IProductDetailsDialog,
)
from src.shared.application.Interfaces.IABCWidget import IABCDialog


class ProductDetailsDialog(IProductDetailsDialog, IABCDialog):
    """Диалог просмотра деталей изделия (только UI)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.product = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Детали изделия")
        self.setGeometry(150, 150, 600, 500)

        layout = QVBoxLayout()

        # Заголовок с названием
        header_layout = QHBoxLayout()
        self.title_label = QLabel("")
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Таблица остатков по филиалам
        self.stock_group_label = QLabel("Остатки по филиалам:")
        layout.addWidget(self.stock_group_label)

        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(3)
        self.stock_table.setHorizontalHeaderLabels(["Филиал", "Склад", "Количество"])
        self.stock_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.stock_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.stock_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.stock_table.setMaximumHeight(150)
        layout.addWidget(self.stock_table)

        # Разделитель
        layout.addWidget(QLabel("Ингредиенты:"))

        # Таблица ингредиентов
        self.ingredients_table = QTableWidget()
        self.ingredients_table.setColumnCount(4)
        self.ingredients_table.setHorizontalHeaderLabels(
            ["Ингредиент", "Количество", "Цена", "Стоимость"]
        )
        self.ingredients_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.ingredients_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.ingredients_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.ingredients_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        layout.addWidget(self.ingredients_table)

        # Общая стоимость
        self.total_cost_label = QLabel("")
        self.total_cost_label.setStyleSheet(
            "font-weight: bold; color: #D32F2F; font-size: 12pt;"
        )
        layout.addWidget(self.total_cost_label)

        # Кнопка закрытия
        buttons_layout = QHBoxLayout()
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close_dialog)
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_btn)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    # Методы для внешнего управления
    def set_product(self, product_name):
        """Устанавливает название продукта"""
        self.title_label.setText(product_name)

    def display_stock(self, stock_items: List[StockItemDisplayDTO]):

        if stock_items:
            self.stock_table.setRowCount(len(stock_items))
            for i, item in enumerate(stock_items):
                self.stock_table.setItem(i, 0, QTableWidgetItem(item.branch_name))
                self.stock_table.setItem(i, 1, QTableWidgetItem(item.warehouse_name))
                self.stock_table.setItem(i, 2, QTableWidgetItem(str(item.quantity)))
        else:
            self.stock_table.setRowCount(1)
            self.stock_table.setItem(
                0, 0, QTableWidgetItem("Продукт ещё не был завезён ни на один склад!")
            )
            self.stock_table.setItem(0, 1, QTableWidgetItem(""))
            self.stock_table.setItem(0, 2, QTableWidgetItem(""))

    def display_ingredients(self, ingredients: List[IngredientDisplayDTO], total_cost):
        self.ingredients_table.setRowCount(len(ingredients))

        for i, ing in enumerate(ingredients):
            self.ingredients_table.setItem(i, 0, QTableWidgetItem(ing.name))
            self.ingredients_table.setItem(i, 1, QTableWidgetItem(str(ing.quantity)))
            self.ingredients_table.setItem(i, 2, QTableWidgetItem(ing.unit))
            self.ingredients_table.setItem(i, 3, QTableWidgetItem(str(ing.unit_cost)))

        self.total_cost_label.setText(f"Общая стоимость изделия: {total_cost:.2f} ₽")

    def close_dialog(self):
        self.accept()
