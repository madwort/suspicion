from hypothesis.stateful import initialize, invariant, rule, precondition, RuleBasedStateMachine
import hypothesis.strategies as st
from hypothesis import assume, settings
import pytest

from calculator.nodes import Add, Subtract, Divide, Value, NaryExpr, BinaryExpr
from calculator.calculator1 import calculate as c1
from calculator.calculator2 import calculate as c2

# build by make the current expr a child node of a new node
# this means we can use isinstance(self.expr) as a precondition
# I think this means that hypothesis will redraw, rather than bailing (as with assume())

@settings(max_examples=5000)
class CalculatorMachine(RuleBasedStateMachine):

    @initialize(value=st.integers(min_value=1, max_value=10))
    def create_root_node(self, value):
        self.expr = Value(value)

    @precondition(lambda self: isinstance(self.expr, NaryExpr))
    @rule(
        value=st.integers(min_value=1, max_value=10),
    )
    def add_value_to_an_nary_node(self, value):
        self.expr.args.append(Value(value))

    @rule(
        value=st.integers(min_value=1, max_value=10),
    )
    def add_an_addition_node(self, value):
        self.expr = Add([self.expr,Value(value)])

    @precondition(lambda self: isinstance(self.expr, NaryExpr))
    @rule()
    def addition_node_rotate_values(self):
        before = self.expr
        newlist = self.expr.args[1:]
        newlist.append(self.expr.args[0])
        self.expr = Add(newlist)

    @rule(
        value=st.integers(min_value=1, max_value=10),
        lhs=st.booleans(),
    )
    def add_a_divide_node_head(self, value, lhs):
        if lhs:
            self.expr = (Divide(self.expr,Value(value)))
        else:
            self.expr = (Divide(Value(value),self.expr))

    # @precondition(lambda self: isinstance(self.expr, BinaryExpr))
    # @rule(
    #     value=st.integers(min_value=1, max_value=10),
    #     lhs=st.booleans(),
    # )
    # def modify_a_divide_node_head(self, value, lhs):
    #     if lhs:
    #         self.expr = (Divide(self.expr.lhs,Value(value)))
    #     else:
    #         self.expr = (Divide(Value(value),self.expr.rhs))

    @invariant()
    def compare_results(self):
        assert c1(self.expr) == c2(self.expr)

TestCalculatorMachine = CalculatorMachine.TestCase

if __name__ == "__main__":
    unittest.main()
