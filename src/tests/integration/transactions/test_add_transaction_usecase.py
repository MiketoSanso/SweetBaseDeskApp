from datetime import datetime

import pytest

from src.features.transactions.application.dtos.TransactionDisplayDTO import (
    TransactionDisplayDTO,
)
from src.features.transactions.application.usecases.AddTransactionUseCase import (
    AddTransactionUseCase,
)
from src.features.transactions.application.value_objects.TransactionItem import (
    TransactionItem,
)


class TestAddTransactionUseCase:
    @pytest.mark.parametrize(
        "is_arrival, branch_id, warehouse_id, items, total_amount, timestamp, user_note, should_success",
        [
            (
                True,
                1,
                1,
                [TransactionItem(product_id=1, quantity=10, product_name="Продукт 0")],
                10,
                datetime.now(),
                "note",
                True,
            ),
            (
                False,
                1,
                1,
                [TransactionItem(product_id=1, quantity=9, product_name="Продукт 0")],
                9,
                datetime.now(),
                "note",
                True,
            ),
            (
                False,
                1,
                1,
                [TransactionItem(product_id=1, quantity=10, product_name="Продукт 0")],
                10,
                datetime.now(),
                "note",
                True,
            ),
            (
                False,
                1,
                1,
                [TransactionItem(product_id=1, quantity=11, product_name="Продукт 0")],
                11,
                datetime.now(),
                "note",
                False,
            ),
            (
                True,
                1,
                -1,
                [TransactionItem(product_id=1, quantity=10, product_name="Продукт 0")],
                10,
                datetime.now(),
                "note",
                False,
            ),
            (
                True,
                -1,
                1,
                [TransactionItem(product_id=1, quantity=10, product_name="Продукт 0")],
                10,
                datetime.now(),
                "note",
                False,
            ),
            (
                True,
                1,
                999,
                [TransactionItem(product_id=1, quantity=10, product_name="Продукт 0")],
                10,
                datetime.now(),
                "note",
                False,
            ),
            (
                True,
                999,
                1,
                [TransactionItem(product_id=1, quantity=10, product_name="Продукт 0")],
                10,
                datetime.now(),
                "note",
                False,
            ),
            (
                True,
                1,
                1,
                [TransactionItem(product_id=1, quantity=10, product_name="Продукт 0")],
                -1,
                datetime.now(),
                "note",
                False,
            ),
            (True, 1, 1, [], 0, datetime.now(), "note", False),
        ],
    )
    def test_add_transaction(
        self,
        dependencies,
        create_products,
        create_branches,
        create_transaction,
        is_arrival,
        branch_id,
        warehouse_id,
        items,
        total_amount,
        timestamp,
        user_note,
        should_success,
    ):
        create_products(3)
        create_branches(1)

        numb_check_trans = 0
        if not is_arrival:
            create_transaction()
            numb_check_trans = 1

        usecase: AddTransactionUseCase = dependencies.add_transaction_usecase
        dto = TransactionDisplayDTO(
            is_arrival=is_arrival,
            branch_id=branch_id,
            warehouse_id=warehouse_id,
            items=items,
            total_amount=total_amount,
            timestamp=timestamp,
            user_note=user_note,
        )

        result = usecase.execute(dto)

        assert result.status is should_success

        if should_success and not is_arrival and items[0].quantity == 10:
            all_stock_items = dependencies.stock_items_repo.get_stock_items(
                items[0].product_id
            )

            assert len(all_stock_items) == 0

        if should_success:
            all_transactions = dependencies.transactions_repo.get_transactions()

            assert all_transactions[numb_check_trans].is_arrival == is_arrival
            assert all_transactions[numb_check_trans].branch_id == branch_id
            assert all_transactions[numb_check_trans].warehouse_id == warehouse_id
            assert all_transactions[numb_check_trans].items == items
            assert all_transactions[numb_check_trans].total_amount == total_amount
            assert all_transactions[numb_check_trans].timestamp == timestamp
            assert all_transactions[numb_check_trans].user_note == user_note
