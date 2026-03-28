from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.BranchesRepository import BranchesRepository


class GetBranchesUseCase:
    def __init__(self, repo: BranchesRepository):
        self.repo = repo

    @usecase_func
    def execute(self) -> ProcessDTO:
        branches = self.repo.get_branches()

        if not branches:
            return ProcessDTO(
                status=False, message="Филиалов нет!", error="Repository returned None"
            )

        return ProcessDTO(status=True, message="Филиалы отправлены.", data=branches)
