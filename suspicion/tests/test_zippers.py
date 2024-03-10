from calculator.nodes import Divide, Multiply, Value
from suspicion.zippers import Location, walk_breadth_first


def test_zipper():
    expr = Divide(
        lhs=Multiply(
            args=[
                Divide(lhs=Value(1), rhs=Value(2)),
                Divide(lhs=Value(3), rhs=Value(4)),
                Divide(lhs=Value(5), rhs=Value(6)),
            ]
        ),
        rhs=Multiply(args=[Value(1), Value(2), Value(3)]),
    )
    loc = Location.from_node(expr)

    loc1 = loc.follow("lhs").follow("args").follow(2)
    assert loc1.node == Divide(lhs=Value(5), rhs=Value(6))

    loc2 = loc1.modify(lambda expr: Value(expr.lhs.value + expr.rhs.value))
    assert loc2.node == Value(11)

    expr2 = loc2.top_node()
    assert expr2 == Divide(
        lhs=Multiply(
            args=[
                Divide(lhs=Value(1), rhs=Value(2)),
                Divide(lhs=Value(3), rhs=Value(4)),
                Value(11),
            ]
        ),
        rhs=Multiply(args=[Value(1), Value(2), Value(3)]),
    )


def test_walk_breadth_first():
    expr = Divide(
        lhs=Multiply(
            args=[
                Divide(lhs=Value(1), rhs=Value(2)),
                Divide(lhs=Value(3), rhs=Value(4)),
                Divide(lhs=Value(5), rhs=Value(6)),
            ]
        ),
        rhs=Multiply(args=[Value(1), Value(2), Value(3)]),
    )

    locs = list(walk_breadth_first(Location.from_node(expr)))
    assert locs
