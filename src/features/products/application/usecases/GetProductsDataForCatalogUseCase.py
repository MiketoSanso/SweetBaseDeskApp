from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.Interfaces.IProductsRepository import IProductsRepository
from src.shared.application.Interfaces.IStockItemsRepository import (
    IStockItemsRepository,
)
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func


class GetProductsDataForCatalogUseCase:
    def __init__(
        self, db_products: IProductsRepository, db_stock_items: IStockItemsRepository
    ):
        self.db_products = db_products
        self.db_stock_items = db_stock_items

    @usecase_func
    def execute(self) -> ProcessDTO:
        products = self.db_products.get_products()

        if products == {}:
            return ProcessDTO(
                status=False,
                message="Продукты не найдены!",
                error="Products are not found!",
            )

        data = []
        for product in products:
            count_stock = self.db_stock_items.get_count_product_in_stocks(
                product.local_id
            )

            data.append(
                {
                    "id": product.local_id,
                    "name": product.name,
                    "stock_count": count_stock,
                }
            )

        return ProcessDTO(status=True, message="Данные получены успешно!", data=data)
