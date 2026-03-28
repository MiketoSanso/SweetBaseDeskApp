from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from src.features.branches.application.interfaces.IBranchesTab import IBranchesTab
from src.shared.application.Interfaces.IABCWidget import IABCWidget


class BranchesTab(IBranchesTab, IABCWidget):
    """Вкладка управления филиалами (только UI)"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Настройка вкладки филиалов"""
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Управление филиалами")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # Информация
        info_label = QLabel(
            "Здесь вы можете добавлять и просматривать филиалы компании."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Кнопка добавления филиала
        self.add_branch_btn = QPushButton("+ Добавить филиал")
        layout.addWidget(self.add_branch_btn)

        # Список филиалов
        self.branches_list = QListWidget()
        layout.addWidget(self.branches_list)

        # Кнопка обновления
        self.refresh_btn = QPushButton("Обновить список")
        layout.addWidget(self.refresh_btn)

        layout.addStretch()
        self.setLayout(layout)

    def set_on_add_branch_requested(self, callback):
        self.add_branch_btn.clicked.connect(callback)

    def set_on_load_branches_requested(self, callback):
        self.refresh_btn.clicked.connect(callback)

    def display_branches(self, branches, is_available):
        """Отображает список филиалов"""
        self.branches_list.clear()

        if not is_available:
            item = QListWidgetItem("Нет филиалов. Добавьте первый филиал!")
            item.setForeground(Qt.gray)
            self.branches_list.addItem(item)
            return

        for branch in branches:
            item_text = f"{branch.name} | Складов: {len(branch.warehouses)}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, branch.local_id)
            self.branches_list.addItem(item)
