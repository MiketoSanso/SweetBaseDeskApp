import pytest

from Dependencies import Dependencies
from src.features.products.application.usecases.GetStockItemsUseCase import (
    GetStockItemsUseCase,
)


class TestGetStockItemsUseCase:
    @pytest.mark.parametrize(
        "product_id, should_have_stock_items, should_succeed",
        [
            (1, True, True),
            (1, False, False),
            (0, True, False),
            (999, True, False),
        ],
    )
    def test_load_stock_items(
        self,
        dependencies: Dependencies,
        setup_initial_stock,
        product_id,
        should_have_stock_items,
        should_succeed,
    ):
        if should_have_stock_items:
            assert setup_initial_stock(3)

        usecase: GetStockItemsUseCase = dependencies.get_stock_items_usecase

        result = usecase.execute(product_id)

        assert result.status is should_succeed
