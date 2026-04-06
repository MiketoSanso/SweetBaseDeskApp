import pytest

from Dependencies import Dependencies
from src.features.branches.application.dtos.BranchCreateDTO import BranchCreateDTO
from src.features.branches.application.usecases.AddBranchUseCase import AddBranchUseCase


class TestAddBranchUseCase:
    @pytest.mark.parametrize(
        "name, warehouses, should_succeed",
        [
            ("Тестовый филиал", [1, 2, 3], True),
            ("Филиал без складов", [], False),
            ("", [1], False),
        ],
    )
    def test_add_branch(self, dependencies, name, warehouses, should_succeed):
        usecase: AddBranchUseCase = dependencies.add_branch_usecase
        dto = BranchCreateDTO(name=name, warehouses=warehouses)

        result = usecase.execute(dto)

        assert result.status is should_succeed

        if should_succeed:
            all_branches = dependencies.branches_repo.get_branches()

            assert all_branches[0].name == name
            assert all_branches[0].warehouses == warehouses

    def test_add_multiple_branches(self, dependencies: Dependencies):
        usecase = dependencies.add_branch_usecase

        usecase.execute(BranchCreateDTO(name="Филиал 1", warehouses=[1]))
        usecase.execute(BranchCreateDTO(name="Филиал 2", warehouses=[1, 2]))
        usecase.execute(BranchCreateDTO(name="Филиал 3", warehouses=[1, 2, 3]))

        all_branches = dependencies.branches_repo.get_branches()
        names = [b.name for b in all_branches]

        assert len(all_branches) == 3
        assert "Филиал 1" in names
        assert "Филиал 2" in names
        assert "Филиал 3" in names
