 

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from src.features.products.application.dtos.ProductIngredientDisplayDTO import (
    ProductIngredientDisplayDTO,
)
from src.features.products.application.interfaces.IAddProductDialog import (
    IAddProductDialog,
)
from src.shared.application.Interfaces.IABCWidget import IABCDialog


class AddProductDialog(IAddProductDialog, IABCDialog):
    """Диалог добавления нового изделия (только UI)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавить новое изделие")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        # Заголовок
        title = QLabel("Новое изделие")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Основные поля
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название изделия")
        form_layout.addRow("Название изделия:", self.name_input)

        layout.addLayout(form_layout)

        # Разделитель
        layout.addWidget(QLabel("Ингредиенты изделия:"))

        # Список выбранных ингредиентов
        self.selected_list = QListWidget()
        layout.addWidget(self.selected_list)

        # Кнопки для ингредиентов
        ing_buttons_layout = QHBoxLayout()

        self.add_ing_btn = QPushButton("+ Добавить ингредиент")

        self.remove_ing_btn = QPushButton("- Удалить ингредиент")

        ing_buttons_layout.addWidget(self.add_ing_btn)
        ing_buttons_layout.addWidget(self.remove_ing_btn)

        layout.addLayout(ing_buttons_layout)

        # Кнопки сохранения/отмены
        buttons_layout = QHBoxLayout()

        self.save_btn = QPushButton("Сохранить изделие")

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def set_on_add_ingredient_requested(self, callback):
        self.add_ing_btn.clicked.connect(callback)

    def set_on_remove_ingredient_requested(self, callback):
        def on_remove_requested():
            current_item = self.selected_list.currentItem()
            if current_item:
                ingredient_id = current_item.data(Qt.UserRole)
                callback(ingredient_id)

        self.remove_ing_btn.clicked.connect(on_remove_requested)

    def set_on_save_product_requested(self, ingredients, callback):
        def on_save_requested():
            data = {
                "name": self.name_input.text().strip(),
                "ingredients": ingredients.copy(),
            }
            callback(data)

        self.save_btn.clicked.connect(on_save_requested)

    def get_name(self):
        return self.name_input.text().strip()

    def close_dialog(self):
        self.accept()

    def update_display(self, ingredients: list[ProductIngredientDisplayDTO]):
        self.selected_list.clear()

        for item in ingredients:
            display_text = (
                f"{item.name}: {item.quantity}. | "
                f"{item.unit} × {item.cost} ₽ = "
                f"{item.cost * item.quantity} ₽"
            )

            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.UserRole, item.id)
            self.selected_list.addItem(list_item)
