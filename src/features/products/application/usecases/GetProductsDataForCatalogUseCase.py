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
        products: list[Product] = self.db_products.get_products()

        if not products:
            return ProcessDTO(
                status=False,
                message="Продукты не найдены!",
                error="Products are not found!",
            )

        product_ids = [product.local_id for product in products]

        stock_item_counts: dict[int, int] = self.db_stock_items.get_all_count_stocks(
            tuple(product_ids)
        )

        display_products: list[ProductDisplayDTO] = []

        for product in products:
            display_products.append(
                ProductDisplayDTO(
                    id=product.local_id,
                    name=product.name,
                    stock_count=stock_item_counts.get(product.local_id, 0),
                )
            )

        return ProcessDTO(
            status=True,
            message="Данные получены успешно!",
            data=tuple(display_products),
        )
