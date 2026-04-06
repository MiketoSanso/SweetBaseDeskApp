from src.features.branches.application.dtos.BranchCreateDTO import BranchCreateDTO
from src.features.branches.domain.entities.Branch import Branch
from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.BranchesRepository import BranchesRepository


class AddBranchUseCase:
    def __init__(self, db: BranchesRepository):
        self.db = db

    @usecase_func
    def execute(self, dto: BranchCreateDTO) -> ProcessDTO:
        if not dto.name:
            return ProcessDTO(
                status=False,
                message="Имя филиала не указано!",
                error="Branch name is not defined!",
            )

        if not dto.warehouses:
            return ProcessDTO(
                status=False,
                message="Склады не указаны!",
                error="Warehouses is not defined!",
            )

        branch = Branch.model_validate(dto)

        self.db.add_branch(branch)

        return ProcessDTO(status=True, message="Филиал успешно создан!")
