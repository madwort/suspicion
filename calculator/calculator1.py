import operator
from functools import reduce, singledispatch

from . import nodes


def calculate(expr):
    try:
        return visit(expr)
    except ZeroDivisionError:
        return None


@singledispatch
def visit(expr):
    assert False, f"Unhandled expression type: {type(expr)}"


@visit.register(nodes.Value)
def visit_value(expr):
    return expr.value


@visit.register(nodes.Add)
def visit_add(expr):
    return reduce(operator.add, (visit(arg) for arg in expr.args))


@visit.register(nodes.Multiply)
def visit_multiply(expr):
    return reduce(operator.mul, (visit(arg) for arg in expr.args))


@visit.register(nodes.Subtract)
def visit_subtract(expr):
    return visit(expr.lhs) - visit(expr.rhs)


@visit.register(nodes.Divide)
def visit_divide(expr):
    return visit(expr.lhs) / visit(expr.rhs)
