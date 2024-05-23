from functools import singledispatch

from . import nodes


def calculate(expr):
    try:
        return eval(buildstr(expr))
    except ZeroDivisionError:
        return None


@singledispatch
def buildstr(expr):
    assert False, f"Unhandled expression type: {type(expr)}"


@buildstr.register(nodes.Value)
def buildstr_value(expr):
    return str(expr.value)


@buildstr.register(nodes.Add)
def buildstr_add(expr):
    return parenthesise(" + ".join(buildstr(arg) for arg in expr.args))


@buildstr.register(nodes.Multiply)
def buildstr_multiply(expr):
    return parenthesise(" * ".join(buildstr(arg) for arg in expr.args))


@buildstr.register(nodes.Subtract)
def buildstr_subtract(expr):
    return parenthesise(f"{buildstr(expr.lhs)} - {buildstr(expr.rhs)}")


@buildstr.register(nodes.Divide)
def buildstr_divide(expr):
    # return f"{buildstr(expr.lhs)} / {buildstr(expr.rhs)}"

    # correct version
    return f"({buildstr(expr.lhs)} / {buildstr(expr.rhs)})"


def parenthesise(s):
    return f"({s})"
