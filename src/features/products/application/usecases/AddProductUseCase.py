from src.features.products.application.dtos.ProductCreateDTO import ProductCreateDTO
from src.features.products.domain.entities.Product import Product
from src.shared.application.dtos.ProcessDTO import ProcessDTO
from src.shared.application.Interfaces.IIngredientsRepository import (
    IIngredientsRepository,
)
from src.shared.application.Interfaces.IProductsRepository import IProductsRepository
from src.shared.application.usecases.Decorators.BaseUseCaseDecorator import usecase_func


class AddProductUseCase:
    def __init__(
        self, db_products: IProductsRepository, db_ingredients: IIngredientsRepository
    ):
        self.db_products = db_products
        self.db_ingredients = db_ingredients

    @usecase_func
    def execute(self, dto: ProductCreateDTO) -> ProcessDTO:
        if not dto.name:
            return ProcessDTO(
                status=False,
                message="Имя продукта не указано!",
                error="Product name is not defined!",
            )

        if not dto.ingredients:
            return ProcessDTO(
                status=False,
                message="Ингредиенты не указаны!",
                error="Ingredients is not defined!",
            )

        for ingredient in dto.ingredients:
            if not self.db_ingredients.get_ingredient_by_id(ingredient.ingredient_id):
                return ProcessDTO(
                    status=False,
                    message="Ингредиент не найден!",
                    error="Ingredient is not found!",
                )

        product = Product.model_validate(dto)

        for ingredient in product.ingredients:
            self.db_ingredients.increment_usage(ingredient.ingredient_id)

        self.db_products.add_product(product)

        return ProcessDTO(status=True, message="Продукт успешно создан!")
