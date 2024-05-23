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
    # this is found
    if isinstance(expr.args[0], nodes.Add):
        if isinstance(expr.args[0].args[0], nodes.Add):
            if isinstance(expr.args[0].args[0].args[0], nodes.Add):
                raise Exception("Four Adds in a row are verboten plz!", expr)

    # this is only found by test_hypothesis_head tests
    if isinstance(expr.args[0], nodes.Add):
        if isinstance(expr.args[0].args[0], nodes.Divide):
            if isinstance(expr.args[0].args[0].rhs, nodes.Add):
                raise Exception("No nesting combo Add-Add-Div-Add plz!", expr)

    # harder version
    # hypothesis only finds this if it doesn't find the others
    if len(expr.args) > 5 and isinstance(expr.args[1], nodes.Add):
        raise Exception("Moar args plz!", expr)

    # this test requires rotating the Add arguments
    if isinstance(expr.args[1], nodes.Add):
        raise Exception("Rotate your owl plz!", expr)

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
