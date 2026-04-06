from datetime import datetime

import pytest

from Dependencies import Dependencies
from src.features.branches.domain.entities.Branch import Branch
from src.features.ingredients.domain.entities.Ingredient import Ingredient
from src.features.products.domain.entities.Product import Product
from src.features.products.domain.value_objects.ProductIngredientVO import (
    ProductIngredientVO,
)
from src.features.stock_info.domain.entities.StockItem import StockItem
from src.features.transactions.application.value_objects.TransactionItem import (
    TransactionItem,
)
from src.features.transactions.domain.entities.Transaction import Transaction


@pytest.fixture
def create_branches(dependencies: Dependencies):
    def _create(count: int) -> list[int]:
        created_ids = []
        for i in range(count):
            branch = Branch(name=f"Test Branch {i}", warehouses=[1, 2, 3])
            dependencies.branches_repo.add_branch(branch)
            created_ids.append(branch.local_id)
        return created_ids

    return _create


@pytest.fixture
def create_ingredients(dependencies: Dependencies):
    def _create(count: int) -> bool:
        for i in range(count):
            ingredient = Ingredient(
                name=f"Test Ingredient {i}",
                unit="kg",
                unit_cost=100.0,
                description="Test ingredient description",
            )
            dependencies.ingredients_repo.add_ingredient(ingredient)

        return True

    return _create


@pytest.fixture
def create_products(dependencies: Dependencies, create_ingredients):
    def _create(count: int) -> bool:
        create_ingredients(3)
        for i in range(count):
            product = Product(
                name=f"Test Product {i}",
                ingredients=[
                    ProductIngredientVO(ingredient_id=1, quantity=10),
                    ProductIngredientVO(ingredient_id=2, quantity=10),
                    ProductIngredientVO(ingredient_id=3, quantity=10),
                ],
            )
            dependencies.products_repo.add_product(product)

        return True

    return _create


@pytest.fixture
def setup_initial_stock(dependencies: Dependencies, create_products, create_branches):
    def _create(count: int) -> bool:
        create_products(count)
        create_branches(1)

        for i in range(1, count + 1):
            stock_item = StockItem(branch_id=1, stock_id=1, product_id=i, quantity=10)
            dependencies.stock_items_repo.add_item_in_stock(stock_item)
        return True

    return _create


@pytest.fixture
def create_transaction(dependencies: Dependencies, setup_initial_stock):
    def _create(
        is_arrival: bool = True,
        branch_id: int = 1,
        warehouse_id: int = 1,
        items: list[TransactionItem] = None,
        total_amount: float = 100.0,
        user_note: str = "Test transaction",
    ) -> bool:
        setup_initial_stock(3)
        if items is None:
            items = [
                TransactionItem(product_id=1, quantity=10, product_name="Test Product")
            ]
        transaction = Transaction(
            is_arrival=is_arrival,
            branch_id=branch_id,
            warehouse_id=warehouse_id,
            items=items,
            total_amount=total_amount,
            timestamp=datetime.now(),
            user_note=user_note,
        )
        dependencies.transactions_repo.log_transaction(transaction)
        return True

    return _create
