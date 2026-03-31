from typing import List

from src.features.products.application.dtos.ProductDisplayDTO import ProductDisplayDTO
from src.features.products.domain.entities.Product import Product
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
        products: List[Product] = self.db_products.get_products()

        if not products:
            return ProcessDTO(
                status=False,
                message="Продукты не найдены!",
                error="Products are not found!",
            )

        product_ids = [product.local_id for product in products]

        stock_item_counts: tuple[int] = self.db_stock_items.get_all_count_stocks(tuple(product_ids))



        return ProcessDTO(status=True, message="Данные получены успешно!", data=products)
