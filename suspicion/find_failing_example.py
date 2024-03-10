from suspicion.generate import generate_expr
from suspicion.simplify import simplify


def find_failing_example(check):
    for ix in range(100):
        expr = generate_expr(ix)
        if check(expr):
            continue

        print(f"Failing seed: {ix}")
        return simplify(expr, check)
