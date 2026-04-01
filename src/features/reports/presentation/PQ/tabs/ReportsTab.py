from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGroupBox, QLabel, QPushButton, QVBoxLayout

from src.features.reports.application.dtos.TransactionsInfoDTO import (
    TransactionsInfoDTO,
)
from src.features.reports.application.interfaces.IReportsTab import IReportsTab
from src.shared.application.Interfaces.IABCWidget import IABCWidget


class ReportsTab(IReportsTab, IABCWidget):
    """Вкладка отчетов (только UI)"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Настройка вкладки отчетов"""
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Отчеты по транзакциям")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # Информация
        info_label = QLabel(
            "Здесь вы можете просматривать отчеты по всем операциям прихода и ухода "
            "с фильтрацией по филиалам, складам и датам."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Кнопка просмотра отчетов
        self.view_reports_btn = QPushButton("📈 Просмотреть отчеты")
        layout.addWidget(self.view_reports_btn)

        # Быстрая статистика
        stats_group = QGroupBox("Быстрая статистика")
        stats_layout = QVBoxLayout()
        self.stats_label = QLabel()
        self.stats_label.setWordWrap(True)
        stats_layout.addWidget(self.stats_label)
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        layout.addStretch()
        self.setLayout(layout)

    def set_on_open_reports_requested(self, callback):
        self.view_reports_btn.clicked.connect(callback)

    def display_stats(self, transactions_info: TransactionsInfoDTO):
        text_date = transactions_info.last_transaction_date
        if transactions_info.last_transaction_date is None:
            text_date = "Транзакций не было!"

        self.stats_label.setText(
            f"Всего транзакций: {transactions_info.total_transactions}\n"
            f"Приходов: {transactions_info.in_count}\n"
            f"Уходов: {transactions_info.out_count}\n"
            f"Последняя транзакция: {text_date}"
        )
