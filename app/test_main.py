from unittest.mock import patch, MagicMock

import pytest
import datetime

from app.main import outdated_products


@pytest.mark.parametrize(
    "mock_date, list_of_products, expected_list_of_products",
    [
        pytest.param(
            datetime.date(2022, 2, 2),
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 2, 10),
                    "price": 600
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 2, 5),
                    "price": 120
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 3, 2),
                    "price": 160
                }
            ],
            [],
            id="Every products are fresh"
        ),
        pytest.param(
            datetime.date(2022, 2, 2),
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 2, 10),
                    "price": 600
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 2, 5),
                    "price": 120
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2021, 12, 30),
                    "price": 160
                }
            ],
            ["duck"],
            id="One product is expired"
        ),
        pytest.param(
            datetime.date(2022, 2, 2),
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2021, 10, 25),
                    "price": 600
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2021, 12, 20),
                    "price": 120
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2021, 12, 30),
                    "price": 160
                }
            ],
            ["salmon", "chicken", "duck"],
            id="Every product is expired"
        ),
        pytest.param(
            datetime.date(2022, 2, 2),
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 10, 25),
                    "price": 600
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 12, 20),
                    "price": 120
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 2, 2),
                    "price": 160
                }
            ],
            [],
            id="Product has same date as expiration"
        ),
        pytest.param(
            datetime.date(2022, 2, 2),
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 10, 25),
                    "price": 600
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 12, 20),
                    "price": 120
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 2, 1),
                    "price": 160
                }
            ],
            ["duck"],
            id="Product with date of expire is yesterday"
        )
    ]
)
@patch("app.main.datetime.date")
def test_correct_work_of_function(
        mock_today: MagicMock,
        mock_date: datetime.date,
        list_of_products: list,
        expected_list_of_products: list
) -> None:
    mock_today.today.return_value = mock_date
    assert outdated_products(list_of_products) == expected_list_of_products
