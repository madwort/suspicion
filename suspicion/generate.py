from dataclasses import dataclass
from random import Random
from types import GenericAlias

from calculator.nodes import Expr, Value


def generate_expr(seed):
    generator = Generator(Random(seed))
    return generator(Expr, 0)


@dataclass
class Generator:
    rnd: Random

    def __call__(self, cls, depth):
        if issubclass(cls, Expr):
            return self.generate_expr(cls, depth)

        if isinstance(cls, GenericAlias):
            return self.generate_list(cls, depth + 1)

        if cls == int:
            return self.generate_int()

        assert False, cls

    def generate_expr(self, cls, depth):
        if cls.__subclasses__():
            subclass = self.pick_subclass(cls, depth)
            return self(subclass, depth + 1)
        else:
            return self.generate_obj(cls, depth + 1)

    def pick_subclass(self, cls, depth):
        if cls == Expr and depth > 10:
            return Value
        return self.rnd.choice(cls.__subclasses__())

    def generate_obj(self, cls, depth):
        kwargs = {
            k: self(v.type, depth + 1) for k, v in cls.__dataclass_fields__.items()
        }
        return cls(**kwargs)

    def generate_list(self, cls, depth):
        assert cls.__origin__ == list
        assert cls.__args__ == (Expr,)
        n = self.rnd.randint(1, 3)
        return [self(Expr, depth + 1) for _ in range(n)]

    def generate_int(self):
        return self.rnd.randint(-10, 10)
