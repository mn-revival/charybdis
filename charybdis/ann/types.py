import dataclasses
import enum
from typing import Union


@dataclasses.dataclass
class BankAddr:
    bank: int
    addr: int


AnnType = Union["ArrayType", "PointerType", "PrimitiveType"]


class PrimitiveType(enum.Enum):
    U8 = "U8"
    U16 = "U16"


@dataclasses.dataclass
class ArrayType:
    type: AnnType
    size: int


@dataclasses.dataclass
class PointerType:
    type: AnnType


@dataclasses.dataclass
class Ann:
    addr: BankAddr
    label: str
    type: AnnType
