"""
Optimized code for calculating the likelihood of an exclusive relationship.
Read the whole project at https://tarro.work/code/the-hannah-montana-problem
"""
import math
from typing import List


def likelihood_of_an_exclusive_relationship_not_optimized(A: List[int], N: int) -> float:
    """The probability that no samples of sizes `A` share a value from a population of size `N`.

    Is not optimized in any way.
    """
    p: float = 1.0
    for i, a in enumerate(A):
        p *= math.comb(N - sum(A[:i]), a) / math.comb(N, A[i])
    return 1.0 - p


def likelihood_of_an_exclusive_relationship_algebraically_optimized(A: List[int], N: int) -> float:
    """The probability that no samples of sizes `A` share a value from a population of size `N`.
    
    Uses an optimized formula.
    """
    _sum: int = 0
    numer: int = 1
    denom: int = 1
    for a in A:
        # This multiplication is comparable to the H function
        denom *= math.prod(range(N - a + 1, N + 1))
        _sum += a

    # This multiplication is comparable to the H function
    numer = math.prod(range(N - _sum + 1, N + 1))
    return 1.0 - numer / denom


def likelihood_of_an_exclusive_relationship_completely_optimized(A: List[int], N: int) -> float:
    """The probability that no samples of sizes `A` share a value from a population of size `N`.

    Uses an optimized formula and algorithm.
    """
    A_sorted: List[int] = sorted(A)
    _sum: int
    numer: int
    denom: int

    # Denominator Computations
    h: int = 1
    last_h = None
    initial_x_of_last_h = N - A_sorted[0] + 1

    # calculating h for the smallest sample size in the sequence
    h = math.prod(range(initial_x_of_last_h, N + 1))

    _sum = A_sorted[0]
    denom = h
    last_h = h

    for a in A_sorted[1:]:
        h = last_h
        initial_x = N - a + 1
        # Calculating h up to the last x used in an h calculation
        h *= math.prod(range(initial_x, initial_x_of_last_h))
        denom *= h
        _sum += a

        # Update memory
        last_h = h
        initial_x_of_last_h = initial_x

    # Numerator Computations
    numer = last_h
    # Calculating h up to the last x used in an h calculation
    numer *= math.prod(range(N - _sum + 1, initial_x_of_last_h))

    return 1.0 - numer / denom
