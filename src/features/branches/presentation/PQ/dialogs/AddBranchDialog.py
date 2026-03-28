from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from src.features.branches.application.interfaces.IAddBranchDialog import (
    IAddBranchDialog,
)
from src.shared.application.Interfaces.IABCWidget import IABCDialog


class AddBranchDialog(IAddBranchDialog, IABCDialog):
    """Диалог добавления нового филиала (только UI)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавить филиал")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()

        # Форма ввода данных
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название филиала")
        form_layout.addRow("Название филиала:", self.name_input)

        self.warehouses_input = QSpinBox()
        self.warehouses_input.setMinimum(1)
        self.warehouses_input.setMaximum(20)
        self.warehouses_input.setValue(1)
        form_layout.addRow("Количество складов:", self.warehouses_input)

        layout.addLayout(form_layout)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.save_btn = QPushButton("Сохранить")

        self.cancel_btn = QPushButton("Отмена")

        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def set_on_branch_data_entered(self, callback):
        def on_data_entered():
            data = {
                "name": self.name_input.text().strip(),
                "warehouses_count": self.warehouses_input.value(),
            }
            callback(data)

        self.save_btn.clicked.connect(on_data_entered)

    def close_dialog(self):
        self.accept()
