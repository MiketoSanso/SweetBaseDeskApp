from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.Interfaces.IProductsRepository import IProductsRepository
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func


class GetProductsUseCase:
    def __init__(self, db: IProductsRepository):
        self.db = db

    @usecase_func
    def execute(self) -> ProcessDTO:
        products = self.db.get_products()

        if not products:
            return ProcessDTO(
                status=False, message="Продуктов нет!", error="Repository returned None"
            )

        return ProcessDTO(status=True, message="Продукты отправлены.", data=products)
