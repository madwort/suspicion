import pytest

from calculator.calculator1 import calculate as c1
from calculator.calculator2 import calculate as c2
from suspicion import find_failing_example


def test_calculate():
    assert find_failing_example(check) is None


def check(expr):
    return pytest.approx(c1(expr)) == pytest.approx(c2(expr))
