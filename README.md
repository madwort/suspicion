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

The motivation for working on this is that we've found that Hypothesis struggles to simplify the queries that we generate when using it to test ehrQL.
(It's very possible we're holding Hypothesis wrong...)
Suspicion understands the tree structures that we use, and has a number of strategies for simplifying trees.

Hypothesis is also something of a black box, so replacing it with something non general purpose may make it easier to understand ehrQL's generative tests.
