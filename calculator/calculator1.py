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
    # # this is found
    # if isinstance(expr.args[0], nodes.Add):
    #     if isinstance(expr.args[0].args[0], nodes.Add):
    #         if isinstance(expr.args[0].args[0].args[0], nodes.Add):
    #             raise Exception("Four Adds in a row are verboten plz!", expr)

    # # this is only found by test_hypothesis_head tests
    # if isinstance(expr.args[0], nodes.Add):
    #     if isinstance(expr.args[0].args[0], nodes.Divide):
    #         if isinstance(expr.args[0].args[0].rhs, nodes.Add):
    #             raise Exception("No nesting combo Add-Add-Div-Add plz!", expr)

    # this test requires rotating the Add arguments
    # if len(expr.args) > 1 and isinstance(expr.args[1], nodes.Add):
    #     raise Exception("Rotate your owl plz!", expr)

    return reduce(operator.add, (visit(arg) for arg in expr.args))


@visit.register(nodes.Multiply)
def visit_multiply(expr):
    # # harder version
    # if len(expr.args) > 5 and isinstance(expr.args[1], nodes.Multiply):
    #     raise Exception("Moar args plz!", expr)

    # # even harder version
    # # this is findable with some rules commented out, add_a_nary_node limited to
    # # multiply & max_examples=5000, stateful_step_count=400
    # # (e.g. 2863 passing examples, 3 failing examples, 565 invalid examples)
    # if len(expr.args) > 4 and isinstance(expr.args[1], nodes.Multiply) and isinstance(expr.args[2], nodes.Divide) and isinstance(expr.args[3], nodes.Add):
    #     raise Exception("OMG can you even make this bro!", expr)

    return reduce(operator.mul, (visit(arg) for arg in expr.args))


@visit.register(nodes.Subtract)
def visit_subtract(expr):
    return visit(expr.lhs) - visit(expr.rhs)


@visit.register(nodes.Divide)
def visit_divide(expr):
    # if isinstance(expr.lhs, nodes.Divide) and isinstance(expr.rhs, nodes.Divide):
    #     raise Exception("Three divides", expr)

    # found in 32sec with mirror or with flip first non-full node
    if (
        isinstance(expr.lhs, nodes.Divide) and
        isinstance(expr.lhs.lhs, nodes.Divide) and
        isinstance(expr.lhs.rhs, nodes.Divide) and
        isinstance(expr.rhs, nodes.Divide) and
        isinstance(expr.rhs.lhs, nodes.Divide) and
        isinstance(expr.rhs.rhs, nodes.Divide)
    ):
        raise Exception("Seven divides", expr)

    # # definitely findable with flip & reflect
    # if (
    #     isinstance(expr.lhs, nodes.Divide) and
    #     isinstance(expr.lhs.lhs, nodes.Divide) and
    #     isinstance(expr.lhs.rhs, nodes.Divide) and
    #     isinstance(expr.lhs.lhs.lhs, nodes.Divide) and
    #     isinstance(expr.lhs.rhs.rhs, nodes.Divide) and
    #     isinstance(expr.rhs, nodes.Divide) and
    #     isinstance(expr.rhs.lhs, nodes.Divide) and
    #     isinstance(expr.rhs.lhs.lhs, nodes.Divide) and
    #     isinstance(expr.rhs.lhs.rhs, nodes.Divide) and
    #     isinstance(expr.rhs.rhs, nodes.Divide) and
    #     # this was findable when starting from seven divides
    #     # I assume it would be starting from a Value, just with more search
    #     isinstance(expr.rhs.rhs.lhs, nodes.Divide) and
    #     isinstance(expr.rhs.rhs.rhs, nodes.Divide)
    # ):
    #     raise Exception("Thirteen divides", expr)

    # this is not findable with flip & reflect
    if (
        isinstance(expr.lhs, nodes.Divide) and
        isinstance(expr.lhs.lhs, nodes.Divide) and
        isinstance(expr.lhs.rhs, nodes.Divide) and
        isinstance(expr.lhs.lhs.lhs, nodes.Divide) and
        # ? I think this is unfindable
        # isinstance(expr.lhs.lhs.rhs, nodes.Divide) and
        # ? I think this is unfindable
        # isinstance(expr.lhs.rhs.lhs, nodes.Divide) and
        isinstance(expr.lhs.rhs.rhs, nodes.Divide) and
        isinstance(expr.rhs, nodes.Divide) and
        isinstance(expr.rhs.lhs, nodes.Divide) and
        isinstance(expr.rhs.rhs, nodes.Divide) and
        isinstance(expr.rhs.lhs.lhs, nodes.Divide) and
        isinstance(expr.rhs.lhs.rhs, nodes.Divide) and
        # this (RRL) is hard but findable:
        # ~2k examples of depth 200 from a balanced tree with 7 Divide nodes
        # ~7k examples of depth 200 from a Value (15mins) (Divide nodes only)
        isinstance(expr.rhs.rhs.lhs, nodes.Divide) and
        isinstance(expr.rhs.rhs.rhs, nodes.Divide)
    ):
        raise Exception("wip divides", expr)

    # # yeah, erm, couldn't find in 20mins with mirror
    # # can we find this with flip_first_non_full_lhs()?
    # if (
    #     isinstance(expr.lhs, nodes.Divide) and
    #     isinstance(expr.lhs.lhs, nodes.Divide) and
    #     isinstance(expr.lhs.rhs, nodes.Divide) and
    #     isinstance(expr.lhs.lhs.lhs, nodes.Divide) and
    #     isinstance(expr.lhs.lhs.rhs, nodes.Divide) and
    #     isinstance(expr.lhs.rhs.lhs, nodes.Divide) and
    #     isinstance(expr.lhs.rhs.rhs, nodes.Divide) and
    #     isinstance(expr.rhs, nodes.Divide) and
    #     isinstance(expr.rhs.lhs, nodes.Divide) and
    #     isinstance(expr.rhs.rhs, nodes.Divide) and
    #     isinstance(expr.rhs.lhs.lhs, nodes.Divide) and
    #     isinstance(expr.rhs.lhs.rhs, nodes.Divide) and
    #     isinstance(expr.rhs.rhs.lhs, nodes.Divide) and
    #     isinstance(expr.rhs.rhs.rhs, nodes.Divide)
    # ):
    #     raise Exception("Fifteen divides", expr)


    return visit(expr.lhs) / visit(expr.rhs)
