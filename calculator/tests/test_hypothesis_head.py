from hypothesis.stateful import initialize, invariant, rule, precondition, RuleBasedStateMachine
import hypothesis.strategies as st
from hypothesis import assume, settings, Verbosity
import pytest

from calculator.nodes import Add, Multiply, Subtract, Divide, Value, NaryExpr, BinaryExpr
from calculator.calculator1 import calculate as c1
from calculator.calculator2 import calculate as c2

# build by make the current expr a child node of a new node
# this means we can use isinstance(self.expr) as a precondition
# I think this means that hypothesis will redraw, rather than bailing (as with assume())

# setting deadline=None because some tests showed timing variability
# "Unreliable test timings! On an initial run, this test took 325.93ms, which exceeded the deadline of 200.00ms, but on a subsequent run it took 5.95 ms, which did not."
@settings(
    max_examples=5000,
    stateful_step_count=400,
    deadline=None,
    # verbosity=Verbosity.debug
)
class CalculatorMachine(RuleBasedStateMachine):

    @initialize(value=st.integers(min_value=0, max_value=9))
    def create_root_node(self, value):
        self.expr = Value(value)

    # --- Nary section ---

    # @precondition(lambda self: isinstance(self.expr, NaryExpr))
    # @rule(
    #     value=st.integers(min_value=10, max_value=19),
    # )
    # def add_value_to_an_nary_node(self, value):
    #     self.expr.args.append(Value(value))
    #
    # # TODO
    # @precondition(lambda self: isinstance(self.expr, NaryExpr))
    # @rule(
    #     value=st.integers(min_value=40, max_value=49),
    #     nary=st.booleans(),
    #     function_choice=st.booleans(),
    # )
    # def mutate_leftmost_param_nary_node(self, value, nary, function_choice):
    #     node_type = type(self.expr)
    #     if nary:
    #         if function_choice:
    #             # TOOD: add a value here?
    #             new_node = Add([self.expr.args[0]])
    #         else:
    #             new_node = Multiply([self.expr.args[0]])
    #     else:
    #         if function_choice:
    #             new_node = Divide(self.expr.args[0], Value(value))
    #         else:
    #             new_node = Subtract(self.expr.args[0], Value(value))
    #     new_args = [new_node]
    #     if len(self.expr.args) > 1:
    #         new_args.extend(self.expr.args[1:])
    #     new_expr = node_type(new_args)
    #     # raise Exception(self.expr, new_expr)
    #     self.expr = new_expr
    #
    # @rule(
    #     add=st.booleans(),
    # )
    # def add_a_nary_node(self, add):
    #     if add:
    #         self.expr = Add([self.expr])
    #     else:
    #         self.expr = Multiply([self.expr])
    #
    # @precondition(lambda self: isinstance(self.expr, NaryExpr))
    # @rule()
    # def nary_node_rotate_values(self):
    #     node_type = type(self.expr)
    #     before = self.expr
    #     newlist = self.expr.args[1:]
    #     newlist.append(self.expr.args[0])
    #     self.expr = node_type(newlist)


    # ---Binary section---

    @rule(
        value=st.integers(min_value=30, max_value=39),
        # divide=st.booleans(),
    )
    # def add_a_binary_node(self, value, divide):
    def add_a_binary_node(self, value):
        divide = True
        if divide:
            self.expr = (Divide(self.expr,Value(value)))
        else:
            self.expr = (Subtract(self.expr,Value(value)))

    @precondition(lambda self: isinstance(self.expr, BinaryExpr))
    @rule()
    def binary_node_rotate_values(self):
        node_type = type(self.expr)
        lhs = self.expr.lhs
        rhs = self.expr.rhs
        self.expr = node_type(rhs, lhs)

    # TODO
    @precondition(lambda self: not isinstance(self.expr, Value))
    # @precondition(bottom left node is a BinaryExpr)
    @rule(
        value=st.integers(min_value=50, max_value=59),
    )
    def add_a_binary_node_bottom_left(self, value):
        current_node = self.expr
        previous_node = self.expr
        while isinstance(current_node, BinaryExpr):
            previous_node = current_node
            current_node = current_node.lhs
        new_node = Divide(current_node, Value(value))
        previous_node.lhs = new_node

    # @precondition(lambda self: isinstance(self.expr, BinaryExpr))
    # @rule()
    # def reflect_a_binary_tree_recursively(self):
    #     def _reflect_a_node(node):
    #         root_type = type(node)
    #         if isinstance(node, Value):
    #             return node
    #         else:
    #             return root_type(_reflect_a_node(node.rhs), _reflect_a_node(node.lhs))
    #     reflected_expr = _reflect_a_node(self.expr)
    #     self.expr = reflected_expr

    # TODO: flip at the first node down the lhs that is not full
    # this fixes seven divides but maybe not 15 divides
    @precondition(lambda self: isinstance(self.expr, BinaryExpr))
    @rule()
    def flip_first_non_full_lhs(self):
        def _walk_to_first_non_full_node(node):
            root_type = type(node)
            # TODO: not needed but just in case
            if isinstance(node, Value):
                return node
            # if one of the args is a Value, flip them
            elif isinstance(node.lhs, Value) or isinstance(node.rhs, Value):
                return root_type(node.rhs, node.lhs)
            # else keep walking down the lhs
            else:
                return root_type(_walk_to_first_non_full_node(node.lhs), node.rhs)
        flipped_expr = _walk_to_first_non_full_node(self.expr)
        # raise Exception(self.expr, flipped_expr)
        self.expr = flipped_expr

    # TODO: do a breadth-first search for the Binary Node closest to the root
    # which is not full 


    # TODO: rotate the leaf nodes (at the leaf Binary level or Value level? or lowest level in a sub-tree?) 

    # --- generic section ---

    # TODO: reflect an entire structure?


    @invariant()
    def compare_results(self):
        try:
            # assert c1(self.expr) == c2(self.expr)
            # bug is in c1 & is a crash
            c1(self.expr)
            
        except AssertionError as exc:
            raise Exception(self.expr, exc)
        except TypeError as exc:
            raise Exception(self.expr, exc)

TestCalculatorMachine = CalculatorMachine.TestCase

if __name__ == "__main__":
    unittest.main()
