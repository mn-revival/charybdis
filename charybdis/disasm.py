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
        ###########
        # LD r, r #
        ###########

        # LD B, r
        case 0b01_000_000:
            # r = B
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.B])
            size = 1
        case 0b01_000_001:
            # r = C
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.C])
            size = 1
        case 0b01_000_010:
            # r = D
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.D])
            size = 1
        case 0b01_000_011:
            # r = E
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.E])
            size = 1
        case 0b01_000_100:
            # r = H
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.H])
            size = 1
        case 0b01_000_101:
            # r = L
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.L])
            size = 1
        case 0b01_000_110:
            # r = [HL]
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.HL])
            size = 1
        case 0b01_000_111:
            # r = A
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.B, insn.R8.A])
            size = 1

        # LD C, r
        case 0b01_001_000:
            # r = B
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.B])
            size = 1
        case 0b01_001_001:
            # r = C
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.C])
            size = 1
        case 0b01_001_010:
            # r = D
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.D])
            size = 1
        case 0b01_001_011:
            # r = E
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.E])
            size = 1
        case 0b01_001_100:
            # r = H
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.H])
            size = 1
        case 0b01_001_101:
            # r = L
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.L])
            size = 1
        case 0b01_001_110:
            # r = [HL]
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.HL])
            size = 1
        case 0b01_001_111:
            # r = A
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.A])
            size = 1

        # LD D, r
        case 0b01_010_000:
            # r = B
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.B])
            size = 1
        case 0b01_010_001:
            # r = C
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.C])
            size = 1
        case 0b01_010_010:
            # r = D
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.D])
            size = 1
        case 0b01_010_011:
            # r = E
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.E])
            size = 1
        case 0b01_010_100:
            # r = H
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.H])
            size = 1
        case 0b01_010_101:
            # r = L
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.L])
            size = 1
        case 0b01_010_110:
            # r = [HL]
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.HL])
            size = 1
        case 0b01_010_111:
            # r = A
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.D, insn.R8.A])
            size = 1

        # LD E, r
        case 0b01_011_000:
            # r = B
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.B])
            size = 1
        case 0b01_011_001:
            # r = C
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.C])
            size = 1
        case 0b01_011_010:
            # r = D
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.D])
            size = 1
        case 0b01_011_011:
            # r = E
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.E])
            size = 1
        case 0b01_011_100:
            # r = H
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.H])
            size = 1
        case 0b01_011_101:
            # r = L
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.L])
            size = 1
        case 0b01_011_110:
            # r = [HL]
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.HL])
            size = 1
        case 0b01_011_111:
            # r = A
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.A])
            size = 1
            
        # LD H, r
        case 0b01_100_000:
            # r = B
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.B])
            size = 1
        case 0b01_100_001:
            # r = C
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.C])
            size = 1
        case 0b01_100_010:
            # r = D
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.D])
            size = 1
        case 0b01_100_011:
            # r = E
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.E])
            size = 1
        case 0b01_100_100:
            # r = H
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.H])
            size = 1
        case 0b01_100_101:
            # r = L
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.L])
            size = 1
        case 0b01_100_110:
            # r = [HL]
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.HL])
            size = 1
        case 0b01_100_111:
            # r = A
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.H, insn.R8.A])
            size = 1
   
        # LD L, r
        case 0b01_101_000:
            # r = B
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.B])
            size = 1
        case 0b01_101_001:
            # r = C
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.C])
            size = 1
        case 0b01_101_010:
            # r = D
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.D])
            size = 1
        case 0b01_101_011:
            # r = E
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.E])
            size = 1
        case 0b01_101_100:
            # r = H
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.H])
            size = 1
        case 0b01_101_101:
            # r = L
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.L])
            size = 1
        case 0b01_101_110:
            # r = [HL]
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.HL])
            size = 1
        case 0b01_101_111:
            # r = A
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.A])
            size = 1

        # LD [HL], r
        case 0b01_110_000:
            # r = B
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.B])
            size = 1
        case 0b01_110_001:
            # r = C
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.C])
            size = 1
        case 0b01_110_010:
            # r = D
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.D])
            size = 1
        case 0b01_110_011:
            # r = E
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.E])
            size = 1
        case 0b01_110_100:
            # r = H
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.H])
            size = 1
        case 0b01_110_101:
            # r = L
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.L])
            size = 1
        case 0b01_110_111:
            # r = A
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.HL, insn.R8.A])
            size = 1


        # LD A, r
        case 0b01_111_000:
            # r = B
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.B])
            size = 1
        case 0b01_111_001:
            # r = C
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.C])
            size = 1
        case 0b01_111_010:
            # r = D
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.D])
            size = 1
        case 0b01_111_011:
            # r = E
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.E])
            size = 1
        case 0b01_111_100:
            # r = H
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.H])
            size = 1
        case 0b01_111_101:
            # r = L
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.L])
            size = 1
        case 0b01_111_110:
            # r = [HL]
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.HL])
            size = 1
        case 0b01_111_111:
            # r = A
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.A])
            size = 1

        case 0b00000000:
            decoded = insn.Insn(name=insn.InsnName.NOP)
        case _:
            pass 
    return DecodedInsn(insn=decoded, size=size) if decoded is not None else None
