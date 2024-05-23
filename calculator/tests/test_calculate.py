import pytest

from calculator.calculator1 import calculate as c1
from calculator.calculator2 import calculate as c2
from suspicion import find_failing_example

from calculator.nodes import Add, Subtract, Value

def test_calculate():
    assert find_failing_example(check) is None


def test_simple():
    expr = Add([Value(1), Value(2)])
    check(expr)
    assert c1(expr) == 3


def check(expr):
    return pytest.approx(c1(expr)) == pytest.approx(c2(expr))
