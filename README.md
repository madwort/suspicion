# Suspicion

This is a prototype for replacing Hypothesis for testing parts of ehrQL.

`calculator` is a small library for doing basic arithmetic.
It contains two implementations for evaluating expressions of the form:

    expr = Add(
        Subtract(Value(1), Value(2)),
        Multiply([Value(3), Value(4), Value(5)]),
    )

One of the implementations contains a bug.

There is a test in `calculator/tests/test_calculate.py` that uses `suspicion.find_failing_example` to

1. find an expression where the implementations give different results, and
2. simplify the expression as much as possible.

```
$ pytest calculator
=================================================================== test session starts ===================================================================
platform linux -- Python 3.12.2, pytest-8.1.1, pluggy-1.4.0
rootdir: /home/inglesp/work/ebmdatalab/suspicion
configfile: pyproject.toml
collected 1 item

calculator/tests/test_calculate.py F                                                                                                                [100%]

======================================================================== FAILURES =========================================================================
_____________________________________________________________________ test_calculate ______________________________________________________________________

    def test_calculate():
>       assert find_failing_example(check) is None
E       assert Divide(lhs=Value(value=1), rhs=Divide(lhs=Value(value=1), rhs=Value(value=2))) is None
E        +  where Divide(lhs=Value(value=1), rhs=Divide(lhs=Value(value=1), rhs=Value(value=2))) = find_failing_example(check)

calculator/tests/test_calculate.py:9: AssertionError
------------------------------------------------------------------ Captured stdout call -------------------------------------------------------------------
Failing seed: 48
================================================================= short test summary info =================================================================
FAILED calculator/tests/test_calculate.py::test_calculate - assert Divide(lhs=Value(value=1), rhs=Divide(lhs=Value(value=1), rhs=Value(value=2))) is None
==================================================================== 1 failed in 0.02s ====================================================================
```

The motivation for working on this is that we've found that Hypothesis struggles to simplify the queries that we generate when using it to test ehrQL.
(It's very possible we're holding Hypothesis wrong...)
Suspicion understands the tree structures that we use, and has a number of strategies for simplifying trees.

Hypothesis is also something of a black box, so replacing it with something non general purpose may make it easier to understand ehrQL's generative tests.
