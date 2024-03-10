import pytest

from calculator.nodes import Add, Subtract, Value
from suspicion import simplify


def test_replace_root_with_child():
    expr = Subtract(
        Subtract(Value(1), Value(2)),
        Add([Value(3), Value(4)]),
    )
    assert_simplifies(
        expr,
        simplify.replace_root_with_child,
        [
            Subtract(Value(1), Value(2)),
            Add([Value(3), Value(4)]),
            Value(1),
            Value(2),
            Value(3),
            Value(4),
        ],
    )


def test_replace_node_with_child():
    expr = Subtract(
        Subtract(Value(1), Value(2)),
        Add([Value(3), Value(4)]),
    )
    assert_simplifies(
        expr,
        simplify.replace_node_with_child,
        [
            Subtract(Value(1), Value(2)),
            Add([Value(3), Value(4)]),
            Subtract(Value(1), Add([Value(3), Value(4)])),
            Subtract(Value(2), Add([Value(3), Value(4)])),
            Subtract(Subtract(Value(1), Value(2)), Value(3)),
            Subtract(Subtract(Value(1), Value(2)), Value(4)),
        ],
    )


def test_replace_node_with_value():
    expr = Subtract(
        Subtract(Value(1), Value(2)),
        Add([Value(3), Value(4)]),
    )
    assert_simplifies(
        expr,
        simplify.replace_node_with_value,
        [
            Value(5),
            Subtract(Value(5), Add([Value(3), Value(4)])),
            Subtract(Subtract(Value(1), Value(2)), Value(5)),
        ],
    )


def test_remove_nodes_from_list():
    expr = Subtract(
        Value(1),
        Add([Value(2), Value(3), Value(4)]),
    )
    assert_simplifies(
        expr,
        simplify.remove_nodes_from_list,
        [
            Subtract(Value(1), Add([Value(2)])),
            Subtract(Value(1), Add([Value(3)])),
            Subtract(Value(1), Add([Value(4)])),
            Subtract(Value(1), Add([Value(2), Value(3)])),
            Subtract(Value(1), Add([Value(2), Value(4)])),
            Subtract(Value(1), Add([Value(3), Value(4)])),
        ],
    )


def test_sublists():
    assert simplify.sublists([1, 2, 3]) == [
        [],
        [1],
        [2],
        [3],
        [1, 2],
        [1, 3],
        [2, 3],
        [1, 2, 3],
    ]


def test_replace_value_with_simpler_value():
    assert_simplifies(
        Subtract(Value(5), Value(1)),
        simplify.replace_value_with_simpler_value,
        [
            Subtract(Value(2), Value(1)),
            Subtract(Value(5), Value(0)),
        ],
    )


@pytest.mark.parametrize(
    "n,simplified",
    [
        (0, 0),
        (1, 0),
        (2, 1),
        (10, 2),
        (-10, 10),
    ],
)
def test_simplify_int(n, simplified):
    assert simplify.simplify_int(n) == simplified


def assert_simplifies(expr, fn, expected):
    assert list(simplify.apply_simplification(expr, fn)) == expected
