from src.features.branches.application.usecases.AddBranchUseCase import AddBranchUseCase
from src.features.branches.application.usecases.GetBranchesUseCase import GetBranchesUseCase
from src.features.ingredients.application.usecases.AddIngredientUseCase import AddIngredientUseCase
from src.features.ingredients.application.usecases.DeleteIngredientUseCase import DeleteIngredientUseCase
from src.features.ingredients.application.usecases.EditIngredientUseCase import EditIngredientUseCase
from src.features.ingredients.application.usecases.GetIngredientByIdUseCase import GetIngredientByIDUseCase
from src.features.ingredients.application.usecases.GetIngredientsUseCase import GetIngredientsUseCase
from src.features.products.application.usecases.AddProductUseCase import AddProductUseCase
from src.features.products.application.usecases.GetProductByIdUseCase import GetProductByIdUseCase
from src.features.products.application.usecases.GetProductsDataForCatalogUseCase import GetProductsDataForCatalogUseCase
from src.features.products.application.usecases.GetProductsUseCase import GetProductsUseCase
from src.features.products.application.usecases.GetStockItemsUseCase import GetStockItemsUseCase
from src.features.reports.application.usecases.GetTransactionsByFiltersUseCase import GetTransactionsByFiltersUseCase
from src.features.reports.application.usecases.GetTransactionsInfoUseCase import GetTransactionsInfoUseCase
from src.features.reports.presentation.controllers.ReportsTabPresenter import ReportsTabPresenter
from src.features.stock_info.application.usecases.LoadStockItemsUseCase import LoadStockItemsUseCase
from src.features.stock_info.presentation.controllers.StockTabPresenter import StockTabPresenter
from src.features.transactions.application.usecases.AddTransactionUseCase import AddTransactionUseCase
from src.features.transactions.application.usecases.GetWarehousesUseCase import GetWarehousesUseCase
from src.features.transactions.presentation.controllers.TransactionTabPresenter import TransactionTabPresenter
from src.shared.application.mediators.AddTransactionMediator import AddTransactionMediator
from src.shared.application.mediators.CreateBranchMediator import CreateBranchMediator
from src.shared.infrastructure.repositories.StockItemsRepository import StockItemsRepository
from src.shared.infrastructure.repositories.TransactionsRepository import TransactionsRepository
from src.shared.infrastructure.Base import Base
from src.shared.infrastructure.Database import Database
from src.shared.infrastructure.repositories.BranchesRepository import BranchesRepository
from src.shared.infrastructure.repositories.IngredientsRepository import IngredientsRepository
from src.shared.infrastructure.repositories.ProductsRepository import ProductsRepository

from src.features.branches.presentation.controllers.BranchTabPresenter import BranchTabPresenter
from src.features.ingredients.presentation.controllers.IngredientTabPresenter import IngredientTabPresenter
from src.features.products.presentation.controllers.ProductsTabPresenter import ProductsTabPresenter
from src.shared.presentation.PQ.QtMessageService import QtMessageService
from src.features._main_window.presentation.PQ.tabs.MainWindow import MainWindow


class Dependencies:
    def __init__(self):
        self.db = Database()
        base = Base()

        self.initialize_data()
        self.initialize_usecases()
        self.initialize_ui()
        self.initialize_presenters()
        self.initialize_mediators()

    def initialize_data(self):
        self.branches_repo = BranchesRepository(self.db)
        self.ingredients_repo = IngredientsRepository(self.db)
        self.products_repo = ProductsRepository(self.db)
        self.transactions_repo = TransactionsRepository(self.db, self.products_repo)
        self.stock_items_repo = StockItemsRepository(self.db)

    def initialize_usecases(self):
        self.add_branch_usecase = AddBranchUseCase(self.branches_repo)
        self.get_branches_usecase = GetBranchesUseCase(self.branches_repo)

        self.add_product_usecase = AddProductUseCase(self.products_repo, self.ingredients_repo)
        self.get_product_by_id_usecase = GetProductByIdUseCase(self.products_repo)
        self.get_products_data_for_catalog_usecase = GetProductsDataForCatalogUseCase(self.products_repo, self.stock_items_repo)
        self.get_products_usecase = GetProductsUseCase(self.products_repo)
        self.get_stock_items_usecase = GetStockItemsUseCase(self.stock_items_repo, self.branches_repo)

        self.add_ingredient_usecase = AddIngredientUseCase(self.ingredients_repo)
        self.get_ingredients_usecase = GetIngredientsUseCase(self.ingredients_repo)
        self.delete_ingredient_usecase = DeleteIngredientUseCase(self.ingredients_repo)
        self.edit_ingredient_usecase = EditIngredientUseCase(self.ingredients_repo)
        self.get_data_ingredient_by_id_usecase = GetIngredientByIDUseCase(self.ingredients_repo)

        self.get_transactions_info_usecase = GetTransactionsInfoUseCase(self.transactions_repo)
        self.get_transactions_by_filters_usecase = GetTransactionsByFiltersUseCase(
            self.transactions_repo,
            self.branches_repo
        )

        self.load_stock_items_usecase = LoadStockItemsUseCase(
            self.stock_items_repo,
            self.products_repo,
            self.ingredients_repo
        )

        self.add_transaction_usecase = AddTransactionUseCase(
            self.transactions_repo,
            self.stock_items_repo,
            self.branches_repo,
            self.products_repo
        )
        self.get_warehouses_usecase = GetWarehousesUseCase(self.branches_repo)

    def initialize_ui(self):
        self.message_service = QtMessageService()
        self.main_window = MainWindow()

    def initialize_presenters(self):
        self.branch_tab_presenter = BranchTabPresenter(
            self.main_window.branches_tab,
            self.message_service,
            self.add_branch_usecase,
            self.get_branches_usecase
        )

        self.ingredients_tab_presenter = IngredientTabPresenter(
            self.main_window.ingredients_tab,
            self.message_service,
            self.add_ingredient_usecase,
            self.get_ingredients_usecase,
            self.delete_ingredient_usecase,
            self.edit_ingredient_usecase,
            self.get_data_ingredient_by_id_usecase
        )

        self.products_tab_presenter = ProductsTabPresenter(
            self.main_window.catalog_tab,
            self.message_service,
            self.get_products_data_for_catalog_usecase,
            self.add_product_usecase,
            self.get_product_by_id_usecase,
            self.get_ingredients_usecase,
            self.get_data_ingredient_by_id_usecase,
            self.get_stock_items_usecase
        )

        self.transaction_tab_presenter = TransactionTabPresenter(
            self.main_window.transaction_tab,
            self.message_service,
            self.add_transaction_usecase,
            self.get_products_usecase,
            self.get_branches_usecase,
            self.get_warehouses_usecase
        )

        self.stock_tab_presenter = StockTabPresenter(
            self.main_window.stock_tab,
            self.message_service,
            self.get_branches_usecase,
            self.get_warehouses_usecase,
            self.load_stock_items_usecase
        )

        self.reports_tab_presenter = ReportsTabPresenter(
            self.main_window.reports_tab,
            self.message_service,
            self.get_transactions_info_usecase,
            self.get_transactions_by_filters_usecase,
            self.get_branches_usecase,
            self.get_warehouses_usecase
        )

    def initialize_mediators(self):
        # При создании филиала -> обновляем список складов в транзакциях
        self.create_branch_mediator = CreateBranchMediator(
            self.branch_tab_presenter,
            self.transaction_tab_presenter
        )

        # При создании транзакции -> обновляем каталог продуктов
        # При создании транзакции -> обновляем информацию о транзакциях в Reports
        self.add_transaction_mediator = AddTransactionMediator(
            self.transaction_tab_presenter,
            self.products_tab_presenter,
            self.reports_tab_presenter
        )