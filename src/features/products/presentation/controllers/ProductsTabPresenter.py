from src.features.ingredients.application.usecases.GetIngredientByIdUseCase import (
    GetIngredientByIDUseCase,
)
from src.features.ingredients.application.usecases.GetIngredientsUseCase import (
    GetIngredientsUseCase,
)
from src.features.products.application.interfaces.ICatalogTab import ICatalogTab
from src.features.products.application.usecases.AddProductUseCase import (
    AddProductUseCase,
)
from src.features.products.application.usecases.GetProductByIdUseCase import (
    GetProductByIdUseCase,
)
from src.features.products.application.usecases.GetProductsDataForCatalogUseCase import (
    GetProductsDataForCatalogUseCase,
)
from src.features.products.application.usecases.GetStockItemsUsecase import (
    GetStockItemsUsecase,
)
from src.features.products.presentation.controllers.AddProductDialogPresenter import (
    AddProductDialogPresenter,
)
from src.features.products.presentation.controllers.ProductDetailsDialogPresenter import (
    ProductDetailsDialogPresenter,
)
from src.features.products.presentation.PQ.dialogs.AddProductDialog import (
    AddProductDialog,
)
from src.features.products.presentation.PQ.dialogs.ProductDetailsDialog import (
    ProductDetailsDialog,
)
from src.shared.application.Interfaces.IMessageService import IMessageService


class ProductsTabPresenter:
    def __init__(
        self,
        view: ICatalogTab,
        message_service: IMessageService,
        get_products_data_for_catalog_usecase: GetProductsDataForCatalogUseCase,
        add_product_usecase: AddProductUseCase,
        get_product_by_id_usecase: GetProductByIdUseCase,
        get_ingredients_usecase: GetIngredientsUseCase,
        get_ingredient_by_id_usecase: GetIngredientByIDUseCase,
        get_stock_items_usecase: GetStockItemsUsecase,
    ):
        self.view = view
        self.message_service = message_service
        self.add_product_usecase = add_product_usecase
        self.get_products_data_for_catalog_usecase = (
            get_products_data_for_catalog_usecase
        )
        self.get_product_by_id_usecase = get_product_by_id_usecase
        self.get_ingredients_usecase = get_ingredients_usecase
        self.get_ingredient_by_id_usecase = get_ingredient_by_id_usecase
        self.get_stock_items_usecase = get_stock_items_usecase

        self._display_products()

        self.view.set_on_add_product_requested(self.on_add_product_requested)
        self.view.set_on_refresh_catalog_requested(self._display_products)
        self.view.set_on_product_selected(self.on_product_selected)

    def on_add_product_requested(self):
        dialog = AddProductDialog()

        presenter = AddProductDialogPresenter(
            view=dialog,
            message_service=self.message_service,
            add_product_usecase=self.add_product_usecase,
            get_ingredients_usecase=self.get_ingredients_usecase,
            get_data_ingredient_by_id=self.get_ingredient_by_id_usecase,
        )

        presenter.set_on_success_callback(self._display_products)

        dialog.exec()

    def on_product_selected(self, id: int):
        dialog = ProductDetailsDialog()

        product = self.get_product_by_id_usecase.execute(id)

        presenter = ProductDetailsDialogPresenter(
            view=dialog,
            message_service=self.message_service,
            get_ingredient_by_id_usecase=self.get_ingredient_by_id_usecase,
            get_stock_items_usecase=self.get_stock_items_usecase,
            product=product.data,
        )

        dialog.exec()

    def on_load_products_requested(self):
        self._display_products()

    def _display_products(self):
        result = self.get_products_data_for_catalog_usecase.execute()

        self.view.display_products(result.data, result.status)
