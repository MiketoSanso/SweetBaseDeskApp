from PySide6.QtWidgets import QTabWidget

from src.features._main_window.application.interfaces.IMainWindow import IMainWindow
from src.features.branches.presentation.PQ.tabs.BranchesTab import BranchesTab
from src.features.ingredients.presentation.PQ.tabs.IngredientsTab import IngredientsTab
from src.features.products.presentation.PQ.tabs.CatalogTab import CatalogTab
from src.features.reports.presentation.PQ.tabs.ReportsTab import ReportsTab
from src.features.stock_info.presentation.PQ.tabs.StockTab import StockTab
from src.features.transactions.presentation.PQ.tabs.TransactionTab import TransactionTab
from src.shared.application.Interfaces.IABCWidget import IABCMainWindow


class MainWindow(IMainWindow, IABCMainWindow):
    """Основное окно приложения (только UI)"""

    def __init__(self):
        super().__init__()

        self._catalog_tab = CatalogTab()
        self._transaction_tab = TransactionTab()
        self._ingredients_tab = IngredientsTab()
        self._branches_tab = BranchesTab()
        self._stock_tab = StockTab()
        self._reports_tab = ReportsTab()

        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("📦 Складская система с филиалами")
        self.setGeometry(100, 100, 1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(self._catalog_tab, "📋 Каталог изделий")
        self.tabs.addTab(self._transaction_tab, "🔄 Приход/Уход")
        self.tabs.addTab(self._ingredients_tab, "🧪 Ингредиенты")
        self.tabs.addTab(self._branches_tab, "🏢 Филиалы")
        self.tabs.addTab(self._stock_tab, "📊 Товары на складе")
        self.tabs.addTab(self._reports_tab, "📈 Отчеты")

    @property
    def catalog_tab(self):
        return self._catalog_tab

    @property
    def transaction_tab(self):
        return self._transaction_tab

    @property
    def ingredients_tab(self):
        return self._ingredients_tab

    @property
    def branches_tab(self):
        return self._branches_tab

    @property
    def stock_tab(self):
        return self._stock_tab

    @property
    def reports_tab(self):
        return self._reports_tab
