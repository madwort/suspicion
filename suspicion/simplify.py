import itertools

from calculator.nodes import Expr, Value

from .zippers import Location, walk_breadth_first


def simplify(expr, test):
    """Find the simplest simplification of expr such that `test(expr)` is False."""

    while True:
        simpler_expr = simplify_once(expr, test)
        if simpler_expr is None:
            return expr
        expr = simpler_expr


def simplify_once(expr, test):
    for simplification in [
        replace_root_with_child,
        replace_node_with_child,
        replace_node_with_value,
        remove_nodes_from_list,
        replace_value_with_simpler_value,
    ]:
        for simpler_expr in apply_simplification(expr, simplification):
            # TODO: cache here
            if not test(simpler_expr):
                return simpler_expr


def apply_simplification(node, fn):
    for loc in walk_breadth_first(Location.from_node(node)):
        yield from fn(loc)


def replace_root_with_child(loc):
    if isinstance(loc.node, Value):
        return

    for child in loc.children():
        if isinstance(child.node, Expr):
            yield child.node


def replace_node_with_child(loc):
    if isinstance(loc.node, Value):
        return

    if isinstance(loc.node, list):
        loc_to_replace = loc.up()
    else:
        loc_to_replace = loc

    for child in loc.children():
        if isinstance(child.node, list):
            continue
        yield loc_to_replace.replace(child.node).top_node()


def replace_node_with_value(loc):
    if isinstance(loc.node, Expr) and not isinstance(loc.node, Value):
        yield loc.replace(Value(5)).top_node()


def remove_nodes_from_list(loc):
    if isinstance(loc.node, list):
        for sublist in sublists(loc.node):
            if len(sublist) in [0, len(loc.node)]:
                continue
            yield loc.replace(sublist).top_node()


def sublists(lst):
    return [
        list(combination)
        for combination in itertools.chain.from_iterable(
            itertools.combinations(lst, n) for n in range(len(lst) + 1)
        )
    ]


def replace_value_with_simpler_value(loc):
    if isinstance(loc.node, Value):
        new_value = Value(simplify_int(loc.node.value))
        yield loc.replace(new_value).top_node()


def simplify_int(n):
    if n == 0:
        return n
    if n == 1:
        return 0
    if n == 2:
        return 1
    if n > 2:
        return 2
    assert n < 0
    return -n
