from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from calculator.nodes import Expr, Value


@dataclass
class Location:
    """A location in a tree.

        node: the node at this location in the tree
        prev: the previous location, towards the root (or None if node is the root)
        key:  the key (either an object attribute name or a list index) to get this
              location's node from the previous location's node

    It is designed to support efficient non-destructive updates to a tree, and is based
    on the Zipper data structure described here: https://learnyouahaskell.com/zippers.
    """

    node: Expr | list[Expr]
    prev: Location | None
    key: str | int | None

    def __post_init__(self):
        # Type-check this!
        if isinstance(self.node, Expr):
            cls = ObjLocation
        elif isinstance(self.node, list):
            cls = ListLocation
        else:
            assert False, type(self.node)
        self.__class__ = cls

    @staticmethod
    def from_node(node):
        return Location(node=node, prev=None, key=None)

    def get_child(self, key):
        raise NotImplementedError

    def child_keys(self):
        raise NotImplementedError

    def build_node(self, child_key, child_node):
        raise NotImplementedError

    def children(self):
        for k in self.child_keys():
            yield self.follow(k)

    def follow(self, key):
        return Location(
            node=self.get_child(key),
            prev=self,
            key=key,
        )

    def up(self):
        return Location(
            node=self.prev.build_node(self.key, self.node),
            prev=self.prev.prev,
            key=self.prev.key,
        )

    def top(self):
        if self.prev:
            return self.up().top()
        return self

    def top_node(self):
        return self.top().node

    def path_to_top(self):
        if self.prev:
            return self.prev.path_to_top() + [self.key]
        return []

    def modify(self, fn):
        return Location(
            node=fn(self.node),
            prev=self.prev,
            key=self.key,
        )

    def replace(self, node):
        return self.modify(lambda _: node)


class ObjLocation(Location):
    def get_child(self, key):
        return getattr(self.node, key)

    def child_keys(self):
        return vars(self.node).keys()

    def build_node(self, child_key, child_node):
        kwargs = {
            k: child_node if k == child_key else v  # comment to preserve formatting
            for k, v in vars(self.node).items()
        }
        return type(self.node)(**kwargs)


class ListLocation(Location):
    def get_child(self, key):
        return self.node[key]

    def child_keys(self):
        return range(len(self.node))

    def build_node(self, child_key, child_node):
        return [
            child_node if ix == child_key else v  # comment to preserve formatting
            for ix, v in enumerate(self.node)
        ]


def walk_breadth_first(location):
    todo = deque([location])
    while todo:
        location = todo.popleft()
        yield location
        if isinstance(location.node, Value):
            continue
        todo.extend(location.children())
