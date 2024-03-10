from dataclasses import dataclass


@dataclass
class Expr: ...


@dataclass
class Value(Expr):
    value: int


@dataclass
class NaryExpr(Expr):
    args: list[Expr]


@dataclass
class BinaryExpr(Expr):
    lhs: Expr
    rhs: Expr


@dataclass
class Add(NaryExpr): ...


@dataclass
class Multiply(NaryExpr): ...


@dataclass
class Subtract(BinaryExpr): ...


@dataclass
class Divide(BinaryExpr): ...
