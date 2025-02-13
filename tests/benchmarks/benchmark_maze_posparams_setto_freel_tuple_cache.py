from collections.abc import Callable, Mapping
import timeit
from itertools import product
from clsp.dsl import DSL
from clsp.enumeration import enumerate_terms, interpret_term
from clsp.fcl import FiniteCombinatoryLogic

from clsp.types import Constructor, Literal, Param, LVar, Type


def plus_one(a: str) -> Callable[[Mapping[str, Literal]], int]:
    def _inner(vars: Mapping[str, Literal]) -> int:
        return int(1 + vars[a].value)

    return _inner


def is_free(pos: tuple[int, int]) -> bool:
    col, row = pos
    SEED = 0
    if row == col:
        return True
    else:
        return pow(11, (row + col + SEED) * (row + col + SEED) + col + 7, 1000003) % 5 > 0


def main(SIZE: int = 10, output: bool = True) -> float:
    U: Callable[[int, int, str], str] = lambda b, _, p: f"{p} => UP({b})"
    D: Callable[[int, int, str], str] = lambda b, _, p: f"{p} => DOWN({b})"
    L: Callable[[int, int, str], str] = lambda b, _, p: f"{p} => LEFT({b})"
    R: Callable[[int, int, str], str] = lambda b, _, p: f"{p} => RIGHT({b})"

    pos: Callable[[str], Type] = lambda ab: Constructor("pos", (LVar(ab)))

    repo: Mapping[
        Callable[[int, int, str], str] | str,
        Param | Type,
    ] = {
        U: DSL(cache=True)
        .Use("a", "int2")
        .Use("b", "int2")
        .As(lambda a: (a[0], a[1] - 1))
        .Use("pos", pos("a"))
        .In(pos("b")),
        D: DSL(cache=True)
        .Use("a", "int2")
        .Use("b", "int2")
        .As(lambda a: (a[0], a[1] + 1))
        .Use("pos", pos("a"))
        .In(pos("b")),
        L: DSL(cache=True)
        .Use("a", "int2")
        .Use("b", "int2")
        .As(lambda a: (a[0] - 1, a[1]))
        .Use("pos", pos("a"))
        .In(pos("b")),
        R: DSL(cache=True)
        .Use("a", "int2")
        .Use("b", "int2")
        .As(lambda a: (a[0] + 1, a[1]))
        .Use("pos", pos("a"))
        .In(pos("b")),
        "START": "pos" @ (Literal((0, 0), "int2")),
    }

    # literals = {"int": list(range(SIZE))}
    literals = {"int2": list(filter(is_free, product(range(SIZE), range(SIZE))))}

    if output:
        for row in range(SIZE):
            for col in range(SIZE):
                if is_free((row, col)):
                    print("-", end="")
                else:
                    print("#", end="")
            print("")

    fin = "pos" @ (Literal((SIZE - 1, SIZE - 1), "int2"))

    fcl: FiniteCombinatoryLogic[Callable[[int, int, str], str] | str] = FiniteCombinatoryLogic(
        repo, literals=literals
    )

    start = timeit.default_timer()
    grammar = fcl.inhabit(fin)

    for term in enumerate_terms(fin, grammar, 3):
        t = interpret_term(term)
        if output:
            print(t)

    return timeit.default_timer() - start


if __name__ == "__main__":
    main()
