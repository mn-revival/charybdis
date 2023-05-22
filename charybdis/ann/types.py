import collections
import dataclasses
import enum
from typing import Optional, Union


@dataclasses.dataclass(frozen=True)
class BankAddr:
    """A unique location in addressable memory"""

    bank: int
    addr: int


AnnType = Union["ArrayType", "CodeType", "ImageType", "PointerType", "PrimitiveType"]


@dataclasses.dataclass(frozen=True)
class CodeType:
    size: int


@dataclasses.dataclass(frozen=True)
class ImageType:
    size: int
    width: Optional[int] = 0


@dataclasses.dataclass(frozen=True)
class ArrayType:
    type: AnnType
    size: int


@dataclasses.dataclass(frozen=True)
class PointerType:
    type: AnnType


class PrimitiveType(enum.Enum):
    U8 = "U8"
    U16 = "U16"


@dataclasses.dataclass(frozen=True)
class Ann:
    """Optionally typed label at a specific address"""

    addr: BankAddr
    label: str
    type: Optional[AnnType]


class AnnMapping:
    anns_at_address: dict[BankAddr, set[Ann]]
    label_addresses: dict[str, BankAddr]

    def __init__(self, anns: list[Ann]) -> None:
        self.anns_at_address = collections.defaultdict(set)
        self.label_addresses = {}
        for ann in anns:
            self.add(ann)

    def add(self, ann: Ann) -> None:
        self.anns_at_address[ann.addr].add(ann)
        if ann.label == "":
            return
        if ann.label in self.label_addresses:
            raise Exception(f"label '{ann.label}' defined twice")
        self.label_addresses[ann.label] = ann.addr

    def has(self, ann: Ann) -> bool:
        return ann in self.anns_at_address[ann.addr]

    def get_label_address(self, label: str) -> Optional[BankAddr]:
        return self.label_addresses.get(label)


def ann(bank: int, addr: int, label: str, type: Optional[AnnType] = None) -> Ann:
    assert bank >= 0 and bank <= 0x1FF
    assert addr >= addr <= 0xFFFF
    return Ann(
        addr=BankAddr(bank=bank, addr=addr),
        label=label,
        type=type,
    )
