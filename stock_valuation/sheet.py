from typing import Generic, TypeVar, Iterator
from collections.abc import Sequence
from dataclasses import dataclass
from abc import ABC


ExpressionT = TypeVar("ExpressionT", bound="Expression")
T = TypeVar("T")


class Series(Generic[ExpressionT]):
    def __init__(self, data: Sequence[ExpressionT]) -> None:
        self._data = list(data)

    def __iter__(self) -> Iterator[ExpressionT]:
        return iter(self._data)

    def __getitem__(self, index: int) -> ExpressionT:
        if isinstance(index, int):
            return self._data[index]

    def append(self, item: ExpressionT) -> None:
        return self._data.append(item)


class Sheet(Generic[ExpressionT]):
    def __init__(self, data_dict: [str, dict[str, ExpressionT]]) -> None:
        self._row_label_index_map = {}
        self._rows = []
        for i, (label, row_data) in enumerate(data_dict.items()):
            if label in self._row_label_index_map:
                raise ValueError("Duplicate row label.")
            self._row_label_index_map[label] = i
            self._rows.append(Series(row_data))

    def __getitem__(self, index: int | str) -> Series[ExpressionT]:
        if isinstance(index, int):
            return self._rows[index]
        if isinstance(index, str):
            return self._rows[self._row_label_index_map[index]]
        else:
            raise TypeError("Unexpected index type.")

    def to_dict(self) -> dict[str, list[ExpressionT]]:
        context = Context(sheet=self)
        return {
            row_label: [expr.eval(context) for expr in self._rows[row_index]]
            for row_label, row_index in self._row_label_index_map.items()
        }

    def get_next_col(self) -> None:
        for row in self._rows:
            row.append(row[-1].copy())


@dataclass(frozen=True)
class CellRef:
    row: int
    col: int


@dataclass(frozen=True)
class Context[T]:
    sheet: Sheet[T]


class Expression(ABC, Generic[T]):
    def eval(self, context: Context[T]) -> T:
        raise NotImplementedError()

    def copy(self) -> "Expression[T]":
        raise NotImplementedError()


class Literal(Expression[T]):
    def __init__(self, value: T) -> None:
        self._value = value

    def eval(self, context: Context[T]) -> T:
        return self._value

    def copy(self) -> "Literal[T]":
        return Literal(self._value)


class Mult(Expression[T]):
    def __init__(self, a: Expression[T], b: Expression[T]) -> None:
        self._a = a
        self._b = b

    def eval(self, context: Context[T]) -> T:
        return self._a.eval(context) * self._b.eval(context)

    def copy(self) -> "Mult[T]":
        return Mult(self._a.copy(), self._b.copy())


class CellRefExpression(Expression[T]):
    def __init__(self, cell_ref: CellRef) -> None:
        self._cell_ref = cell_ref

    def eval(self, context: Context[T]) -> T:
        return context.sheet[self._cell_ref.row][self._cell_ref.col].eval(context)

    def copy(self) -> "CellRefExpression[T]":  # TODO: take offset
        return CellRefExpression(CellRef(row=self._cell_ref.row, col=self._cell_ref.col + 1))


class Sum(Expression[T]):
    def __init__(self, addends: Sequence[Expression[T]]) -> None:
        self._addends = addends

    def eval(self, context: Context[T]) -> T:
        return sum(addend.eval(context) for addend in self._addends)

    def copy(self) -> "Sum[T]":
        return Sum(list(addend.copy() for addend in self._addends))
