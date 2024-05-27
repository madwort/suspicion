import hypothesis.strategies as st
import hypothesis as hyp
from hypothesis import assume, event, settings, Verbosity
from hypothesis.control import current_build_context

from calculator.nodes import Add, Multiply, Subtract, Divide, Value, NaryExpr, BinaryExpr
from calculator.calculator1 import calculate as c1

MAX_DEPTH=10

def depth_exceeded():
    ctx = current_build_context()
    return ctx.data.depth > MAX_DEPTH

@st.composite
def calculator_strategy(draw):
    all_strategies = [
        value_strategy,
        # add_strategy,
        # multiply_strategy,
        # subtract_strategy,
        divide_strategy,
    ]
    if depth_exceeded():
        my_strategy = value_strategy
    else:
        my_strategy = draw(st.sampled_from(all_strategies))
    return draw(my_strategy())

@st.composite
def value_strategy(draw):
    return draw(st.builds(Value, st.integers(min_value=0, max_value=10)))

@st.composite
def list_of_values(draw):
    # TODO: make longer lists!
    first = draw(value_strategy())
    return [first]

def add_strategy():
    return nary_strategy(Add)

def multiply_strategy():
    return nary_strategy(Multiply)

@st.composite
def nary_strategy(draw, expr):
    return draw(st.builds(expr, list_of_values()))

def subtract_strategy():
    return binary_strategy(Subtract)

def divide_strategy():
    return binary_strategy(Divide)

@st.composite
def binary_strategy(draw, expr):
    lhs = calculator_strategy()
    rhs = calculator_strategy()
    return draw(st.builds(expr, lhs, rhs))

@settings(max_examples=100000)
@hyp.given(
    calc=calculator_strategy()
)
def test_c1(calc):
    c1(calc)
