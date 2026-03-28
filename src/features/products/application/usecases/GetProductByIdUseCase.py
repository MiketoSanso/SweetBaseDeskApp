from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.Interfaces.IProductsRepository import IProductsRepository
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func


class GetProductByIdUseCase:
    def __init__(self, db: IProductsRepository):
        self.db = db

    @usecase_func
    def execute(self, id: int) -> ProcessDTO:
        product = self.db.get_product_by_id(id)

        if not product:
            return ProcessDTO(
                status=False, message="Продукт не найден!", error="Product not found!"
            )

        return ProcessDTO(status=True, message="Продукт найден успешно!", data=product)
