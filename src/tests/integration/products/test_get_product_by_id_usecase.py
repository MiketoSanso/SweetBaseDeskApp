import pytest

from src.features.products.application.dtos.ProductCreateDTO import ProductCreateDTO
from src.features.products.application.usecases.AddProductUseCase import (
    AddProductUseCase,
)
from src.features.products.application.usecases.GetProductByIdUseCase import (
    GetProductByIdUseCase,
)
from src.features.products.domain.value_objects.ProductIngredientVO import (
    ProductIngredientVO,
)


class TestGetProductByIDUseCase:
    @pytest.mark.parametrize(
        "id, should_success",
        [(1, True), (-1, False), (9999999, False)],
    )
    def test_get_ingredient_by_id(
        self, dependencies, create_products, id, should_success
    ):
        assert create_products(1)

        usecase: GetProductByIdUseCase = dependencies.get_product_by_id_usecase
        result = usecase.execute(id)

        assert result.status is should_success
