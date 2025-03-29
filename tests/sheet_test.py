import pytest

from stock_valuation.sheet import Sheet, Literal, Mult, CellRefExpression, CellRef, Sum


@pytest.fixture
def data_dict():
    return {
        "revenue": [10, 11, 12],
        "cost": [6, 8, 7],
        "gross_profit": [4, 3, 5],
    }


# @pytest.fixture
# def data_matrix():
#     return [
#         [10, 11, 12],
#         [6, 8, 7],
#         [4, 3, 5],
#     ]


def test_getitem_by_int(data_dict):
    sheet = Sheet(data_dict)

    assert sheet[0][0] == 10
    assert sheet[0][1] == 11
    assert sheet[0][2] == 12
    assert sheet[1][0] == 6
    assert sheet[1][1] == 8
    assert sheet[1][2] == 7
    assert sheet[2][0] == 4
    assert sheet[2][1] == 3
    assert sheet[2][2] == 5


# def test_getitem_by_str(data_dict):
#     sheet = Sheet(data_dict)
#
#     assert sheet["revenue"][0] == 10
#     assert sheet["revenue"][1] == 11
#     assert sheet["revenue"][2] == 12
#     assert sheet["cost"][0] == 6
#     assert sheet["cost"][1] == 8
#     assert sheet["cost"][2] == 7
#     assert sheet["gross_profit"][0] == 4
#     assert sheet["gross_profit"][1] == 3
#     assert sheet["gross_profit"][2] == 5


def test_mult():
    sheet = Sheet({
        "a": [
            Literal(1),
            Mult(
                Literal(1.2),
                CellRefExpression(CellRef(row=0, col=0)),
            ),
            Mult(
                Literal(1.2),
                CellRefExpression(CellRef(row=0, col=1)),
            )
        ]
    })

    result = sheet.to_dict()

    assert result == {
        "a": [1, 1.2, 1.44]
    }


@pytest.mark.parametrize("data, expected", [
    (
        {
            "a": [
                Literal(1),
                Mult(
                    Literal(1.2),
                    CellRefExpression(CellRef(0, 0)),
                ),
            ]
        },
        {
            "a": [1, 1.2, 1.44]
        }
    ),
    (
        {
            "a": [
                Literal(1),
                Mult(
                    Literal(2),
                    CellRefExpression(CellRef(0, 0)),
                ),
            ],
            "b": [
                Literal(2),
                Mult(
                    Literal(3),
                    CellRefExpression(CellRef(1, 0)),
                ),
            ],
            "c": [
                Sum([
                    CellRefExpression(CellRef(0, 0)),
                    CellRefExpression(CellRef(1, 0)),
                ]),
                Sum([
                    CellRefExpression(CellRef(0, 1)),
                    CellRefExpression(CellRef(1, 1)),
                ]),
            ],
        },
        {
            "a": [1, 2, 4],
            "b": [2, 6, 18],
            "c": [3, 8, 22],
        }
    )
])
def test_gen_next_col(data, expected):
    sheet = Sheet(data)

    sheet.get_next_col()
    result = sheet.to_dict()

    assert result == expected










