import pytest

from Dependencies import Dependencies
from src.features.reports.application.usecases.GetTransactionsInfoUseCase import (
    GetTransactionsInfoUseCase,
)


class TestGetTransactionsInfoUseCase:
    @pytest.mark.parametrize(
        "should_have_transactions",
        [
            (True),
            (False),
        ],
    )
    def test_load_stock_items(
        self, dependencies: Dependencies, create_transaction, should_have_transactions
    ):
        if should_have_transactions:
            assert create_transaction()

        usecase: GetTransactionsInfoUseCase = dependencies.get_transactions_info_usecase

        result = usecase.execute()

        is_transactions_loaded = result.data.total_transactions > 0
        assert is_transactions_loaded == should_have_transactions
