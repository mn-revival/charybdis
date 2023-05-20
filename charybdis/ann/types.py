import dataclasses
import enum
from typing import Optional, Union


@dataclasses.dataclass
class BankAddr:
    """A unique location in addressable memory"""

    bank: int
    addr: int


AnnType = Union["ArrayType", "CodeType", "ImageType", "PointerType", "PrimitiveType"]


@dataclasses.dataclass
class CodeType:
    size: int


@dataclasses.dataclass
class ImageType:
    size: int
    width: Optional[int] = 0


@dataclasses.dataclass
class ArrayType:
    type: AnnType
    size: int


@dataclasses.dataclass
class PointerType:
    type: AnnType


class PrimitiveType(enum.Enum):
    U8 = "U8"
    U16 = "U16"


@dataclasses.dataclass
class Ann:
    """Optionally typed label at a specific address"""

    addr: BankAddr
    label: str
    type: Optional[AnnType]


def ann(bank: int, addr: int, label: str, type: Optional[AnnType] = None) -> Ann:
    assert bank >= 0 and bank <= 0x1FF
    assert addr >= addr <= 0xFFFF
    return Ann(
        addr=BankAddr(bank=bank, addr=addr),
        label=label,
        type=type,
    )
