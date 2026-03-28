from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout

from src.features.ingredients.application.interfaces.IIngredientsTab import (
    IIngredientsTab,
)
from src.shared.application.Interfaces.IABCWidget import IABCWidget


class IngredientsTab(IIngredientsTab, IABCWidget):
    """Вкладка управления ингредиентами (только UI)"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Настройка вкладки"""
        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Управление ингредиентами")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # Информация
        info_label = QLabel(
            "Здесь вы можете добавлять, редактировать и удалять ингредиенты, "
            "которые используются в изделиях."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # Кнопка управления
        self.manage_btn = QPushButton("📁 Открыть управление ингредиентами")
        layout.addWidget(self.manage_btn)

        # Статистика
        self.stats_label = QLabel()
        layout.addWidget(self.stats_label)

        layout.addStretch()
        self.setLayout(layout)

    def set_on_manage_ingredients_requested(self, callback):
        self.manage_btn.clicked.connect(callback)

    def update_stats(self, count):
        """Обновляет отображение статистики"""
        self.stats_label.setText(f"Всего ингредиентов в системе: {count}")
