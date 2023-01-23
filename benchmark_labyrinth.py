from dataclasses import dataclass, field
from typing import Callable

from cls_python import *
from cls_python.fcl import FiniteCombinatoryLogic

labyrinth_free = (
    (True, False, True, True, True, True, True, False, True, True, True, True, True, False, True, False, True, True, True, False, True, True, True, False, True, True, True, False, True, True),
    (True, True, True, True, True, True, True, True, True, False, True, False, False, True, True, False, False, True, True, True, True, True, True, True, True, True, False, False, False, True),
    (True, True, True, True, True, True, True, False, True, False, True, True, True, True, False, True, True, True, True, True, False, False, True, True, False, True, True, False, True, False),
    (True, True, True, True, True, False, True, True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False),
    (True, True, True, True, True, False, True, True, False, False, True, False, True, False, True, True, False, True, True, True, True, True, True, False, True, True, True, True, True, False),
    (True, True, False, False, True, True, True, True, False, True, True, True, True, True, False, True, True, True, False, True, True, True, True, True, False, True, True, True, True, True),
    (True, True, True, False, True, False, False, True, True, False, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True),
    (True, True, True, False, True, False, False, True, True, False, False, False, True, True, True, True, False, True, True, True, False, True, True, True, True, False, True, True, False, True),
    (True, True, True, False, True, True, False, True, True, False, True, False, True, True, False, False, False, True, False, True, True, True, True, True, False, False, True, False, True, True),
    (True, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, False, True, True, True, True, True, True, True, False, False, True, False, True, True),
    (True, False, True, False, True, True, False, True, True, True, True, True, True, True, True, False, True, True, True, False, True, False, True, False, True, True, False, False, True, False),
    (True, True, True, False, True, True, True, True, True, False, True, True, True, True, True, False, True, True, False, False, True, False, True, True, True, True, True, True, True, True),
    (True, False, True, True, False, False, True, False, False, True, True, True, False, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True),
    (True, True, True, False, True, True, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, False, True, True, True),
    (False, True, True, False, True, True, False, True, True, True, True, True, False, True, True, False, True, True, True, False, True, True, True, False, True, True, True, True, True, True),
    (True, False, False, True, True, True, False, False, True, True, False, False, True, True, False, True, True, False, False, True, True, True, True, True, True, True, False, True, True, True),
    (True, True, False, False, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True),
    (True, True, True, True, True, True, True, True, True, True, False, False, True, True, True, False, False, False, True, False, True, True, True, True, True, True, True, True, True, True),
    (True, True, True, True, True, False, True, True, True, False, True, False, False, True, True, True, True, True, False, True, True, True, True, True, True, True, True, False, False, True),
    (False, False, True, True, False, True, False, True, True, False, False, True, False, True, True, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True),
    (True, True, True, False, False, False, True, False, True, True, True, True, True, False, True, True, True, True, True, True, True, True, False, True, False, True, True, True, True, False),
    (False, True, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, False, False, True),
    (True, True, True, True, True, False, True, True, True, True, True, True, True, True, False, True, False, True, True, False, True, True, True, True, True, True, True, True, True, True),
    (True, True, True, False, True, True, True, True, False, True, True, False, True, True, True, True, True, False, True, True, False, True, True, True, True, False, True, False, True, True),
    (True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, False, False, True, True, True),
    (True, True, True, False, True, True, False, True, True, True, True, False, True, True, True, True, True, True, False, False, True, True, True, True, False, True, True, True, False, True),
    (False, False, True, True, False, True, True, True, True, False, True, True, True, False, True, True, False, False, True, True, True, True, True, True, True, True, False, False, False, True),
    (True, True, True, True, True, True, True, False, True, False, True, False, True, False, True, True, False, False, False, True, True, True, True, True, True, True, True, True, True, True),
    (True, True, False, True, False, True, True, True, True, True, False, True, True, True, True, True, False, True, True, False, False, True, False, True, False, True, True, False, True, True),
    (True, True, True, True, True, False, True, True, False, False, False, True, True, False, False, True, False, False, True, True, True, False, True, True, True, True, True, True, True, True)
)

size = 10  # len(labyrinth_free)

zero = Constructor("Z")


def succ(x: Type) -> Type:
    return Constructor("S", x)


def free(pos_row: Type, pos_col: Type) -> Type:
    return Constructor("Free", Product(pos_row, pos_col))


def pos(row: Type, col: Type) -> Type:
    return Constructor("Pos", Product(row, col))


def int_to_type(x: int) -> Type:
    result = zero
    for i in range(0, x):
        result = succ(result)
    return result


free_fields = {
    f"Pos_at_({row}, {col})": free(int_to_type(row), int_to_type(col))
    for row in range(0, size) for col in range(0, size) if labyrinth_free[row][col]
}


def move(drow_from: int, dcol_from: int, drow_to: int, dcol_to: int) -> Type:
    return Type.intersect([
        Arrow(pos(int_to_type(row + drow_from), int_to_type(col + dcol_from)),
              Arrow(
                  free(int_to_type(row + drow_to), int_to_type(col + dcol_to)),
                  pos(int_to_type(row + drow_to), int_to_type(col + dcol_to)))
              )
        for row in range(0, size) for col in range(0, size)
    ])


@dataclass(frozen=True)
class Move(object):
    direction: field(init=True)

    def __call__(self, path: str) -> Callable[[str], str]:
        return lambda _: f"{path} then go {self.direction}"


repository = {
    "start": pos(int_to_type(0), int_to_type(0)),
    Move("up"): move(0, 1, 0, 0),
    Move("down"): move(0, 0, 0, 1),
    Move("left"): move(1, 0, 0, 0),
    Move("right"): move(0, 0, 1, 0),
    **free_fields
}

import timeit

if __name__ == "__main__":
    start = timeit.default_timer()
    gamma = FiniteCombinatoryLogic(repository, Subtypes({}))
    print('Time (Constructor): ', timeit.default_timer() - start) 
    start = timeit.default_timer()
    results = gamma.inhabit(pos(int_to_type(size - 1), int_to_type(size - 1)))
    print('Time (Inhabitation): ', timeit.default_timer() - start) 
    for i in range(0, 3):
        print(results.evaluated[i])




