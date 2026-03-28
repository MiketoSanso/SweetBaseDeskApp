from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from src.features.ingredients.application.interfaces.IAddIngredientDialog import (
    IAddIngredientDialog,
)
from src.features.ingredients.domain.entities.Ingredient import Ingredient
from src.shared.application.Interfaces.IABCWidget import IABCDialog


class AddOrEditIngredientDialog(IAddIngredientDialog, IABCDialog):
    """Диалог добавления нового ингредиента (только UI)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавить ингредиент")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # Форма ввода данных
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название ингредиента")
        form_layout.addRow("Название:", self.name_input)

        self.cost_input = QDoubleSpinBox()
        self.cost_input.setMinimum(0.0)
        self.cost_input.setMaximum(1000000.0)
        self.cost_input.setDecimals(2)
        self.cost_input.setSuffix(" ₽")
        form_layout.addRow("Стоимость за единицу:", self.cost_input)

        self.unit_input = QLineEdit()
        self.unit_input.setText("шт.")
        form_layout.addRow("Единица измерения:", self.unit_input)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)
        self.desc_input.setPlaceholderText("Описание (необязательно)")
        form_layout.addRow("Описание:", self.desc_input)

        layout.addLayout(form_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.save_btn = QPushButton("Сохранить")

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def set_on_ingredient_data_entered(self, callback):
        def on_ingredient_entered():
            data = {
                "name": self.name_input.text().strip(),
                "unit_cost": self.cost_input.value(),
                "unit": self.unit_input.text().strip(),
                "description": self.desc_input.toPlainText().strip(),
            }
            callback(data)

        self.save_btn.clicked.connect(on_ingredient_entered)

    # Методы для предзаполнения (редактирование)
    def set_data(self, ingredient: Ingredient):
        self.name_input.setText(ingredient.name)
        self.cost_input.setValue(ingredient.unit_cost)
        self.unit_input.setText(ingredient.unit)
        self.desc_input.setPlainText(ingredient.description)

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "unit_cost": self.cost_input.value(),
            "unit": self.unit_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
        }

    def close_dialog(self):
        self.accept()
