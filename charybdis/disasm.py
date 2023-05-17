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
    match byte:
        # NOP
        case 0x00:
            decoded = insn.Insn(name=insn.InsnName.NOP)
        # LD B, B
        case 0x40: 
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.B])
        # LD B, C
        case 0x41:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.C])
        # LD B, D
        case 0x42:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.D])
        # LD B, E
        case 0x43:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.E])
        # LD B, H
        case 0x44:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.H])
        # LD B, L
        case 0x45:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.L])
        # LD B, [HL]
        case 0x46:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.HL])
        # LD B, A
        case 0x47:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.A])
        # LD C, B
        case 0x48:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.B])
        # LD C, C
        case 0x49:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.C])
        # LD C, D
        case 0x4a:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.D])
        # LD C, E
        case 0x4b:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.E])
        # LD C, H
        case 0x4c:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.H])
        # LD C, L
        case 0x4d:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.L])
        # LD C, [HL]
        case 0x4e:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.HL])
        # LD C, A
        case 0x4f:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.A])
        # LD D, B
        case 0x50:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.B])
        # LD D, C
        case 0x51:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.C])
        # LD D, D
        case 0x52:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.D])
        # LD D, E
        case 0x53:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.E])
        # LD D, H
        case 0x54:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.H])
        # LD D, L
        case 0x55:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.L])
        # LD D, [HL]
        case 0x56:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.HL])
        # LD D, A
        case 0x57:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.A])
        # LD E, B
        case 0x58:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.B])
        # LD E, C
        case 0x59:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.C])
        # LD E, D
        case 0x5a:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.D])
        # LD E, E
        case 0x5b:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.E])
        # LD E, H
        case 0x5c:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.H])
        # LD E, L
        case 0x5d:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.L])
        # LD E, [HL]
        case 0x5e:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.HL])
        # LD E, A
        case 0x5f:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.A])
        # LD H, B
        case 0x60:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.B])
        # LD H, C
        case 0x61:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.C])
        # LD H, D
        case 0x62:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.D])
        # LD H, E
        case 0x63:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.E])
        # LD H, H
        case 0x64:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.H])
        # LD H, L
        case 0x65:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.L])
        # LD H, [HL]
        case 0x66:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.HL])
        # LD H, A
        case 0x67:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.A])
        # LD L, B
        case 0x68:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.B])
        # LD L, C
        case 0x69:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.C])
        # LD L, D
        case 0x6a:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.D])
        # LD L, E
        case 0x6b:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.E])
        # LD L, H
        case 0x6c:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.H])
        # LD L, L
        case 0x6d:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.L])
        # LD L, [HL]
        case 0x6e:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.HL])
        # LD L, A
        case 0x6f:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.A])
        # LD [HL], B
        case 0x70:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.B])
        # LD [HL], C
        case 0x71:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.C])
        # LD [HL], D
        case 0x72:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.D])
        # LD [HL], E
        case 0x73:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.E])
        # LD [HL], H
        case 0x74:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.H])
        # LD [HL], L
        case 0x75:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.L])
        # LD [HL], A
        case 0x77:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.A])
        # LD A, B
        case 0x78:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.B])
        # LD A, C
        case 0x79:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.C])
        # LD A, D
        case 0x7a:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.D])
        # LD A, E
        case 0x7b:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.E])
        # LD A, H
        case 0x7c:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.H])
        # LD A, L
        case 0x7d:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.L])
        # LD A, [HL]
        case 0x7e:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.HL])
        # LD A, A
        case 0x7f:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.A])

    return DecodedInsn(insn=decoded, size=size) if decoded is not None else None
