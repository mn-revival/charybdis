import dataclasses
from typing import Optional

from charybdis import insn


@dataclasses.dataclass
class DecodedInsn:
    insn: insn.Insn
    size: int


def decode_insn(rom: bytes, index: int) -> Optional[DecodedInsn]:
    decoded = None
    byte = rom[index]
    size = 1
    if byte == 0x00:
        decoded = insn.Insn(name=insn.InsnName.NOP)
    return DecodedInsn(insn=decoded, size=size) if decoded is not None else None
