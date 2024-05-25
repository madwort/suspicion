from hypothesis.stateful import initialize, invariant, rule, precondition, RuleBasedStateMachine
import hypothesis.strategies as st
from hypothesis import assume, event, settings, Verbosity
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
    max_examples=10000,
    stateful_step_count=200,
    deadline=None,
    # verbosity=Verbosity.debug
)
class CalculatorMachine(RuleBasedStateMachine):

    @initialize(value=st.integers(min_value=0, max_value=9))
    def create_root_node(self, value):
        # select which types of Nodes to investigate
        self.enable_nary = True
        self.enable_binary = False

        # start with a value
        self.expr = Value(value)

        # # start with a binary tree of 7 binary nodes
        # self.expr = Divide(
        #     Divide(Divide(Value(0), Value(1)),Divide(Value(1), Value(2))),
        #     Divide(Divide(Value(2), Value(3)),Divide(Value(3), Value(4)))
        # )

    # --- Nary section ---

    @precondition(lambda self: self.enable_nary)
    @precondition(lambda self: isinstance(self.expr, NaryExpr))
    @rule(
        value=st.integers(min_value=10, max_value=19),
    )
    def add_value_to_an_nary_node(self, value):
        self.expr.args.append(Value(value))

    def walk_to_bottom_left_expr(self):
        current_node = self.expr
        previous_node = self.expr
        while not isinstance(current_node, Value):
            previous_node = current_node
            if isinstance(current_node, BinaryExpr):
                current_node = current_node.lhs
            elif isinstance(current_node, NaryExpr):
                current_node = current_node.args[0]
            else:
                assert False
        return (current_node, previous_node)

    @precondition(lambda self: self.enable_nary)
    @precondition(lambda self: not isinstance(self.expr, Value))
    @rule(
        value=st.integers(min_value=60, max_value=69),
    )
    def add_a_nary_node_bottom_left(self, value):
        current_node, previous_node = self.walk_to_bottom_left_expr()

        new_node = Add([current_node, Value(value)])

        if isinstance(previous_node, BinaryExpr):
            previous_node.lhs = new_node
        elif isinstance(previous_node, NaryExpr):
            previous_node.args[0] = new_node
        else:
            assert False
        event("add_a_nary_node_bottom_left")

    @precondition(lambda self: self.enable_nary)
    @rule(
        add=st.booleans(),
    )
    def add_a_nary_node(self, add):
        if add:
            self.expr = Add([self.expr])
        else:
            self.expr = Multiply([self.expr])

    @precondition(lambda self: self.enable_nary)
    @precondition(lambda self: isinstance(self.expr, NaryExpr))
    @rule()
    def nary_node_rotate_values(self):
        node_type = type(self.expr)
        before = self.expr
        newlist = self.expr.args[1:]
        newlist.append(self.expr.args[0])
        self.expr = node_type(newlist)


    @precondition(lambda self: self.enable_nary)
    @precondition(lambda self: not isinstance(self.expr, Value))
    @rule()
    def nary_node_rotate_values_bottom_left(self):
        current_node = self.expr
        previous_node = self.expr
        previous_previous_node = self.expr
        while not isinstance(current_node, Value):
            previous_previous_node = previous_node
            previous_node = current_node
            if isinstance(current_node, BinaryExpr):
                current_node = current_node.lhs
            elif isinstance(current_node, NaryExpr):
                current_node = current_node.args[0]
            else:
                assert False

        # could make this a precondition, but ok to make a no-op for now
        # & hope that hypothesis will shrink it away?
        if not isinstance(previous_node, NaryExpr):
            return

        node_type = type(previous_node)
        before = previous_node
        newlist = previous_node.args[1:]
        newlist.append(previous_node.args[0])

        if isinstance(previous_previous_node, NaryExpr):
            previous_previous_node.args[0] = node_type(newlist)
        elif isinstance(previous_previous_node, BinaryExpr):
            previous_previous_node.lhs = node_type(newlist)
        else:
            assert False

    # ---Binary section---

    @precondition(lambda self: self.enable_binary)
    @rule(
        value=st.integers(min_value=30, max_value=39),
        # divide=st.booleans(),
    )
    # def add_a_binary_node_head(self, value, divide):
    def add_a_binary_node_head(self, value):
        divide = True
        if divide:
            self.expr = (Divide(self.expr,Value(value)))
        else:
            self.expr = (Subtract(self.expr,Value(value)))

    @precondition(lambda self: self.enable_binary)
    @precondition(lambda self: isinstance(self.expr, BinaryExpr))
    @rule()
    def binary_node_rotate_values(self):
        node_type = type(self.expr)
        lhs = self.expr.lhs
        rhs = self.expr.rhs
        self.expr = node_type(rhs, lhs)

    @precondition(lambda self: self.enable_binary)
    @precondition(lambda self: not isinstance(self.expr, Value))
    @rule(
        value=st.integers(min_value=50, max_value=59),
    )
    def add_a_binary_node_bottom_left(self, value):
        current_node, previous_node = self.walk_to_bottom_left_expr()

        new_node = Divide(current_node, Value(value))

        if isinstance(previous_node, BinaryExpr):
            previous_node.lhs = new_node
        elif isinstance(previous_node, NaryExpr):
            previous_node.args[0] = new_node
        else:
            assert False
        event("add_a_binary_node_bottom_left")



    # # TODO: flip at the first node down the lhs that is not full
    # # this fixes seven divides but maybe not 15 divides
    # @precondition(lambda self: isinstance(self.expr, BinaryExpr))
    # @rule()
    # def flip_first_non_full_lhs(self):
    #     def _walk_to_first_non_full_node(node):
    #         root_type = type(node)
    #         # TODO: not needed but just in case
    #         if isinstance(node, Value):
    #             return node
    #         # if one of the args is a Value, flip them
    #         elif isinstance(node.lhs, Value) or isinstance(node.rhs, Value):
    #             return root_type(node.rhs, node.lhs)
    #         # else keep walking down the lhs
    #         else:
    #             return root_type(_walk_to_first_non_full_node(node.lhs), node.rhs)
    #     flipped_expr = _walk_to_first_non_full_node(self.expr)
    #     # raise Exception(self.expr, flipped_expr)
    #     self.expr = flipped_expr

    # TODO: do a breadth-first search for the Binary Node closest to the root
    # which is not full 

    # TODO: rotate the leaf nodes (at the leaf Binary level or Value level? or lowest level in a sub-tree?) 

    # --- generic section ---

    # Value is fine, just unnecessary
    @precondition(lambda self: not isinstance(self.expr, Value))
    @rule()
    def reflect_a_structure_recursively(self):
        def _reflect_a_node(node):
            root_type = type(node)
            if isinstance(node, Value):
                return node
            elif isinstance(node, BinaryExpr):
                return root_type(_reflect_a_node(node.rhs), _reflect_a_node(node.lhs))
            elif isinstance(node, NaryExpr):
                # reverse the list in place because we can, but we also need to be able
                # to rotate the bottom left NaryExpr
                node.args.reverse()
                return root_type(node.args)
            else:
                assert False
        reflected_expr = _reflect_a_node(self.expr)
        self.expr = reflected_expr

    # --- events ---

    def some_binary_shape_events(self):
        if (
            isinstance(self.expr, Divide) and
            isinstance(self.expr.lhs, Divide) and
            isinstance(self.expr.rhs, Divide)
        ):
            event("Three divides")
        if (
            isinstance(self.expr, Divide) and
            isinstance(self.expr.lhs, Divide) and
            isinstance(self.expr.lhs.lhs, Divide) and
            isinstance(self.expr.lhs.rhs, Divide) and
            isinstance(self.expr.rhs, Divide) and
            isinstance(self.expr.rhs.lhs, Divide) and
            isinstance(self.expr.rhs.rhs, Divide)
        ):
            event("Seven divides")


    @invariant()
    def compare_results(self):
        if self.enable_binary:
            self.some_binary_shape_events()

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
