import pytest

from Dependencies import Dependencies
from src.features.stock_info.application.usecases.LoadStockItemsUseCase import (
    LoadStockItemsUseCase,
)


class TestLoadStockItemsUseCase:
    @pytest.mark.parametrize(
        "branch_id, warehouse_id, have_transactions, should_succeed",
        [
            (1, 1, True, True),
            (-1, 1, True, False),
            (1, -1, True, False),
            (999, 1, True, False),
            (1, 999, True, False),
            (1, 1, False, False),
        ],
    )
    def test_load_stock_items(
        self,
        dependencies: Dependencies,
        create_transactions,
        branch_id,
        warehouse_id,
        have_transactions,
        should_succeed,
    ):
        if have_transactions:
            create_transactions(3)

        usecase: LoadStockItemsUseCase = dependencies.load_stock_items_usecase

        result = usecase.execute(branch_id, warehouse_id)

        assert result.status is should_succeed

        if should_succeed:
            assert result.data is not None
            assert len(result.data) == 3
            assert result.data[0].product_name == "Продукт 0"
        else:
            assert result.error is not None
