from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout

from src.features.stock_info.application.interfaces.IStockTab import IStockTab
from src.shared.application.Interfaces.IABCWidget import IABCWidget


class StockTab(IStockTab, IABCWidget):
    """Вкладка просмотра товаров на складе (только UI)"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Настройка вкладки"""
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Просмотр товаров на складе")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # Информация
        info_label = QLabel(
            "Здесь вы можете просматривать остатки товаров на конкретных складах филиалов."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Кнопка просмотра
        self.view_stock_btn = QPushButton("📊 Просмотреть товары на складе")
        layout.addWidget(self.view_stock_btn)

        # Статистика
        self.stats_label = QLabel()
        layout.addWidget(self.stats_label)

        layout.addStretch()
        self.setLayout(layout)

    def set_on_open_stock_dialog_requested(self, callback):
        self.view_stock_btn.clicked.connect(callback)

    def display_stats(self, branches_count, products_count):
        """Обновляет статистику"""
        self.stats_label.setText(
            f"Филиалов в системе: {branches_count}\n"
            f"Товаров в каталоге: {products_count}"
        )
