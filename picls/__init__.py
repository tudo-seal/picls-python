from collections.abc import Hashable, Iterable, Mapping
from typing import Any, Optional, TypeVar

from .grammar import ParameterizedTreeGrammar

from .subtypes import Subtypes
from .types import Type, Omega, Constructor, Product, Arrow, Intersection
from .enumeration import enumerate_terms, interpret_term, enumerate_terms_of_size
from .fcl import FiniteCombinatoryLogic

__all__ = [
    "Subtypes",
    "Type",
    "Omega",
    "Constructor",
    "Product",
    "Arrow",
    "Intersection",
    "enumerate_terms",
    "enumerate_terms_of_size",
    "interpret_term",
    "FiniteCombinatoryLogic",
    "inhabit_and_interpret",
]

T = TypeVar("T", bound=Hashable, covariant=True)
C = TypeVar("C")


def inhabit_and_interpret(
    repository: Mapping[C, Type],
    query: list[Type] | Type,
    max_count: Optional[int] = 100,
    subtypes: Optional[Mapping[str, set[str]]] = None,
) -> Iterable[Any]:
    fcl = FiniteCombinatoryLogic(repository, {} if subtypes is None else subtypes)

    if not isinstance(query, list):
        query = [query]

    grammar: ParameterizedTreeGrammar[Type, C] = fcl.inhabit(*query)

    for q in query:
        enumerated_terms = enumerate_terms(
            start=q, grammar=grammar, max_count=max_count
        )
        for term in enumerated_terms:
            yield interpret_term(term)
