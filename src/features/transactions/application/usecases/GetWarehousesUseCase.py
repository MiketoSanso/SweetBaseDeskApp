from src.shared.application.dtos.ObjectDisplayDTO import ObjectDisplayDTO
from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func
from src.shared.infrastructure.repositories.BranchesRepository import BranchesRepository


class GetWarehousesUseCase:
    def __init__(self, db: BranchesRepository):
        self.db = db

    @usecase_func
    def execute(self, id: int) -> ProcessDTO:
        if not id or id < 1:
            return ProcessDTO(
                status=False, message="id некорректный!!", error="Id incorrec!"
            )

        branch = self.db.get_branch_by_id(id)

        if not branch:
            return ProcessDTO(
                status=False, message="Филиал не найден!", error="Branch are not found!"
            )

        warehouses = branch.warehouses

        warehouses_dto: list[ObjectDisplayDTO] = []
        for warehouse in warehouses:
            warehouse_dto = ObjectDisplayDTO(
                object_id=warehouse, object_name=f"Склад_{warehouse}"
            )
            warehouses_dto.append(warehouse_dto)

        return ProcessDTO(
            status=True, message="Данные сформированы успешно!", data=warehouses_dto
        )
