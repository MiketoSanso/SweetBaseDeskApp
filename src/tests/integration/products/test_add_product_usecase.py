import pytest

from src.features.products.application.dtos.ProductCreateDTO import ProductCreateDTO
from src.features.products.application.usecases.AddProductUseCase import (
    AddProductUseCase,
)
from src.features.products.domain.value_objects.ProductIngredientVO import (
    ProductIngredientVO,
)


class TestAddProductUseCase:
    @pytest.mark.parametrize(
        "name, ingredients, should_success",
        [
            (
                "Имя",
                [
                    ProductIngredientVO(ingredient_id=1, quantity=1),
                    ProductIngredientVO(ingredient_id=2, quantity=1),
                ],
                True,
            ),
            (
                "",
                [
                    ProductIngredientVO(ingredient_id=1, quantity=1),
                    ProductIngredientVO(ingredient_id=2, quantity=1),
                ],
                False,
            ),
            ("Имя", [], False),
        ],
    )
    def test_add_product(
        self, dependencies, create_ingredients, name, ingredients, should_success
    ):
        assert create_ingredients(2)

        usecase: AddProductUseCase = dependencies.add_product_usecase
        dto = ProductCreateDTO(name=name, ingredients=ingredients)

        result = usecase.execute(dto)

        assert result.status is should_success

        if should_success:
            all_products = dependencies.products_repo.get_products()

            assert all_products[0].name == name
            assert all_products[0].ingredients == ingredients

    def test_add_multiple_products(self, dependencies, create_ingredients):
        ingredients: list[ProductIngredientVO] = [
            ProductIngredientVO(ingredient_id=1, quantity=1),
            ProductIngredientVO(ingredient_id=2, quantity=1),
        ]

        assert create_ingredients(2)

        usecase: AddProductUseCase = dependencies.add_product_usecase
        usecase.execute(dto=ProductCreateDTO(name="Имя 1", ingredients=ingredients))

        usecase.execute(dto=ProductCreateDTO(name="Имя 2", ingredients=ingredients))

        usecase.execute(dto=ProductCreateDTO(name="Имя 3", ingredients=ingredients))

        all_products = dependencies.products_repo.get_products()
        names = [p.name for p in all_products]

        assert len(names) == 3
        assert "Имя 1" in names
        assert "Имя 2" in names
        assert "Имя 3" in names
