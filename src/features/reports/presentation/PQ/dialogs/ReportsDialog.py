from PySide6.QtCore import QDate
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from src.features.branches.domain.entities.Branch import Branch
from src.features.reports.application.dtos.ReportTransactionDTO import (
    ReportTransactionDTO,
)
from src.features.reports.application.interfaces.IReportsDialog import IReportsDialog
from src.shared.application.dtos.ObjectDisplayDTO import ObjectDisplayDTO
from src.shared.application.Interfaces.IABCWidget import IABCDialog


class ReportsDialog(IReportsDialog, IABCDialog):
    """Диалог для просмотра отчетов по транзакциям (только UI)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Отчеты по транзакциям")
        self.setGeometry(100, 100, 900, 600)

        layout = QVBoxLayout()

        # Фильтры
        filters_group = QGroupBox("Фильтры")
        filters_layout = QVBoxLayout()

        # Тип операции
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Тип операции:"))
        self.type_combo = QComboBox()
        self.type_combo.addItem("Все", None)
        self.type_combo.addItem("Приход", True)
        self.type_combo.addItem("Уход", False)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        filters_layout.addLayout(type_layout)

        # Филиал
        branch_layout = QHBoxLayout()
        branch_layout.addWidget(QLabel("Филиал:"))
        self.branch_combo = QComboBox()
        self.branch_combo.addItem("Все", None)
        branch_layout.addWidget(self.branch_combo)
        branch_layout.addStretch()
        filters_layout.addLayout(branch_layout)

        # Склад
        warehouse_layout = QHBoxLayout()
        warehouse_layout.addWidget(QLabel("Склад:"))
        self.warehouse_combo = QComboBox()
        self.warehouse_combo.addItem("Все", None)
        warehouse_layout.addWidget(self.warehouse_combo)
        warehouse_layout.addStretch()
        filters_layout.addLayout(warehouse_layout)

        # Даты
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("С:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.setCalendarPopup(True)
        date_layout.addWidget(self.date_from)

        date_layout.addWidget(QLabel("По:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        date_layout.addWidget(self.date_to)

        date_layout.addStretch()
        filters_layout.addLayout(date_layout)

        # Кнопка применения фильтров
        self.apply_btn = QPushButton("Применить фильтры")
        filters_layout.addWidget(self.apply_btn)

        filters_group.setLayout(filters_layout)
        layout.addWidget(filters_group)

        # Таблица транзакций
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(7)
        self.transactions_table.setHorizontalHeaderLabels(
            ["Дата", "Тип", "Филиал", "Склад", "Товары", "Количество", "Примечание"]
        )
        self.transactions_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.transactions_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.transactions_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.transactions_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        self.transactions_table.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.Stretch
        )
        self.transactions_table.horizontalHeader().setSectionResizeMode(
            5, QHeaderView.ResizeToContents
        )
        self.transactions_table.horizontalHeader().setSectionResizeMode(
            6, QHeaderView.Stretch
        )

        layout.addWidget(self.transactions_table)

        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close_dialog)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def _collect_filters(self):
        """Собирает текущие значения фильтров"""
        filters = {}

        filters["is_arrival"] = self.type_combo.currentData()
        filters["branch_id"] = self.branch_combo.currentData() or 0
        filters["warehouse_id"] = self.warehouse_combo.currentData() or 0

        if self.date_from.date():
            date = self.date_from.date()
            filters["date_from"] = (
                f"{date.year():04d}-{date.month():02d}-{date.day():02d} 00:00:00"
            )
        else:
            filters["date_from"] = None

        if self.date_to.date():
            date = self.date_to.date()
            filters["date_to"] = (
                f"{date.year():04d}-{date.month():02d}-{date.day():02d} 23:59:59"
            )
        else:
            filters["date_to"] = None
        return filters

    def set_on_filters_changed(self, callback):
        def on_apply():
            filters = self._collect_filters()
            callback(filters)

        self.apply_btn.clicked.connect(on_apply)

    def set_on_branch_changed(self, callback):
        def on_changed():
            branch_id = self.branch_combo.currentData()
            callback(branch_id)

        self.branch_combo.currentIndexChanged.connect(on_changed)

    # Методы для внешнего управления
    def set_branches(self, branches: list[Branch], has_branches):
        """Заполняет список филиалов"""
        self.branch_combo.clear()
        self.branch_combo.addItem("Все", None)
        if has_branches:
            for branch in branches:
                self.branch_combo.addItem(branch.name, branch.local_id)

    def set_warehouses(self, warehouses: list[ObjectDisplayDTO]):
        """Заполняет список складов"""
        self.warehouse_combo.clear()
        self.warehouse_combo.addItem("Все", None)
        for wh in warehouses:
            self.warehouse_combo.addItem(f"{wh.object_name}", wh.object_id)

    def display_transactions(self, transactions: list[ReportTransactionDTO]):
        """Отображает транзакции в таблице"""
        if not transactions:
            self.transactions_table.setRowCount(0)
            return

        self.transactions_table.setRowCount(len(transactions))
        for row, t in enumerate(transactions):
            self.transactions_table.setItem(row, 0, QTableWidgetItem(str(t.timestamp)))
            type_item = QTableWidgetItem(t.type)
            type_item.setForeground(QColor("black"))
            self.transactions_table.setItem(row, 1, QTableWidgetItem(t.type))
            self.transactions_table.setItem(row, 2, QTableWidgetItem(t.branch_name))
            self.transactions_table.setItem(row, 3, QTableWidgetItem(t.warehouse_name))
            self.transactions_table.setItem(row, 4, QTableWidgetItem(t.items_text))
            self.transactions_table.setItem(
                row, 5, QTableWidgetItem(str(t.total_amount))
            )
            self.transactions_table.setItem(row, 6, QTableWidgetItem(t.user_note))

    def close_dialog(self):
        self.accept()
