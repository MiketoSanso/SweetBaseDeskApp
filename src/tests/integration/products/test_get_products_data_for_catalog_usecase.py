import pytest

from src.features.products.application.usecases.GetProductsDataForCatalogUseCase import (
    GetProductsDataForCatalogUseCase,
)


class TestGetProductsDataForCatalogUseCase:
    @pytest.mark.parametrize(
        "products_received, should_success",
        [
            (True, True),
            (False, False),
        ],
    )
    def test_get_products_data_for_catalog_usecase(
        self, dependencies, create_products, products_received, should_success
    ):
        if products_received:
            assert create_products(1)

        usecase: GetProductsDataForCatalogUseCase = (
            dependencies.get_products_data_for_catalog_usecase
        )
        result = usecase.execute()

        assert result.status is should_success

        if products_received:
            assert result.data is not None
            assert len(result.data) == 1
