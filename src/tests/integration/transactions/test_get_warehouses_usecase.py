import pytest

from Dependencies import Dependencies
from src.features.transactions.application.usecases.GetWarehousesUseCase import (
    GetWarehousesUseCase,
)


class TestGetWarehousesUseCase:
    @pytest.mark.parametrize(
        "branch_id, should_have_branch, should_succeed",
        [
            (1, True, True),
            (-1, True, False),
            (1, False, False),
            (999, True, False),
        ],
    )
    def test_load_stock_items(
        self,
        dependencies: Dependencies,
        create_branches,
        branch_id,
        should_have_branch,
        should_succeed,
    ):
        if should_have_branch:
            assert create_branches(1)

        usecase: GetWarehousesUseCase = dependencies.get_warehouses_usecase

        result = usecase.execute(branch_id)

        assert result.status is should_succeed

        if result.status:
            branches_repo = dependencies.branches_repo

            branch = branches_repo.get_branch_by_id(branch_id)

            assert branch.warehouses == [1, 2, 3]
