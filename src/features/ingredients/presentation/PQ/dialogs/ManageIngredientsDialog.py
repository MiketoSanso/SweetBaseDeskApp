from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from src.features.ingredients.application.interfaces.IManageIngredientsDialog import (
    IManageIngredientsDialog,
)
from src.shared.application.Interfaces.IABCWidget import IABCDialog


class ManageIngredientsDialog(IManageIngredientsDialog, IABCDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.quantity_input = None
        self._on_ingredient_selected_callback = None
        self.init_ui()
        self.set_mode_management()

    def init_ui(self):
        self.setWindowTitle("Управление ингредиентами")
        self.setGeometry(150, 150, 600, 500)

        layout = QVBoxLayout()

        # Заголовок и кнопки
        header_layout = QHBoxLayout()
        title = QLabel("Ингредиенты")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        self.add_btn = QPushButton("+ Новый ингредиент")
        self.edit_btn = QPushButton("✏️ Редактировать")
        self.delete_btn = QPushButton("🗑️ Удалить")
        self.select_btn = QPushButton("Выбрать")

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.add_btn)
        header_layout.addWidget(self.edit_btn)
        header_layout.addWidget(self.delete_btn)
        header_layout.addWidget(self.select_btn)

        layout.addLayout(header_layout)

        # Список ингредиентов
        self.ingredients_list = QListWidget()
        layout.addWidget(self.ingredients_list)

        # Количество
        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel("Количество:"))
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(10000)
        self.quantity_input.setValue(1)
        quantity_layout.addWidget(self.quantity_input)
        quantity_layout.addStretch()
        layout.addLayout(quantity_layout)

        self.setLayout(layout)

        # Подключение кнопок
        self.add_btn.clicked.connect(self._on_add)
        self.edit_btn.clicked.connect(self._on_edit)
        self.delete_btn.clicked.connect(self._on_delete)
        self.select_btn.clicked.connect(self._on_select)

    def set_mode_management(self):
        self.add_btn.show()
        self.edit_btn.show()
        self.delete_btn.show()
        self.select_btn.hide()
        self.quantity_input.parent().hide()
        self.setWindowTitle("Управление ингредиентами")

    def set_mode_selection(self, with_quantity: bool = False):
        self.add_btn.hide()
        self.edit_btn.hide()
        self.delete_btn.hide()
        self.select_btn.show()

        if with_quantity:
            self.quantity_input.parent().show()
            self.setWindowTitle("Выберите ингредиент и укажите количество")
        else:
            self.quantity_input.parent().hide()
            self.setWindowTitle("Выберите ингредиент")

    def set_on_add_ingredient_requested(self, callback):
        self._on_add_callback = callback

    def set_on_edit_ingredient_requested(self, callback):
        self._on_edit_callback = callback

    def set_on_delete_ingredient_requested(self, callback):
        self._on_delete_callback = callback

    def set_on_ingredient_selected(self, callback):
        self._on_ingredient_selected_callback = callback

    def display_ingredients(self, ingredients, has_ingredients):
        self.ingredients_list.clear()

        if not has_ingredients:
            item = QListWidgetItem("Нет ингредиентов. Добавьте первый!")
            item.setForeground(Qt.gray)
            self.ingredients_list.addItem(item)
            return

        for ing in ingredients:
            item_text = f"{ing.name} - {ing.unit_cost} ₽/{ing.unit}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, ing.local_id)
            self.ingredients_list.addItem(item)

    def close_dialog(self):
        self.accept()

    def _on_add(self):
        if hasattr(self, "_on_add_callback"):
            self._on_add_callback()

    def _on_edit(self):
        if hasattr(self, "_on_edit_callback"):
            current = self.ingredients_list.currentItem()
            if current:
                self._on_edit_callback(current.data(Qt.UserRole))

    def _on_delete(self):
        if hasattr(self, "_on_delete_callback"):
            current = self.ingredients_list.currentItem()
            if current:
                self._on_delete_callback(current.data(Qt.UserRole))

    def _on_select(self):
        if hasattr(self, "_on_ingredient_selected_callback"):
            current = self.ingredients_list.currentItem()
            if current and str(current.data(Qt.UserRole)).isdigit():
                ing_id = current.data(Qt.UserRole)
                quantity = self.quantity_input.value()
                self._on_ingredient_selected_callback(ing_id, quantity)
                self.accept()
