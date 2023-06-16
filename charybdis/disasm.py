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
        # LD BC, nn
        case 0x01:
            size = 3
            imm16 = load_u16(rom, index + 1)
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R16.BC, imm16])
        # LD [BC], A
        case 0x02:
            decoded = insn.Insn(
                name=insn.InsnName.LD,
                operands=[insn.IndirectR16(insn.R16.BC), insn.R8.A],
            )
        # LD B, n
        case 0x06:
            size = 2
            imm = rom[index + 1]
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R8.B, insn.U8(imm)]
            )
        # RLCA
        case 0x07:
            decoded = insn.Insn(name=insn.InsnName.RLCA)
        # LD [nn], SP
        case 0x08:
            size = 3
            addr = load_u16(rom, index + 1)
            decoded = insn.Insn(
                name=insn.InsnName.LD,
                operands=[insn.DirectU16(addr), insn.R16.SP],
            )
        # LD A, [BC]
        case 0x0A:
            decoded = insn.Insn(
                name=insn.InsnName.LD,
                operands=[insn.R8.A, insn.IndirectR16(insn.R16.BC)],
            )
        # LD C, n
        case 0x0E:
            size = 2
            imm = rom[index + 1]
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R8.C, insn.U8(imm)]
            )
        # RRCA
        case 0x0F:
            decoded = insn.Insn(name=insn.InsnName.RRCA)
        # LD DE, nn
        case 0x11:
            size = 3
            imm16 = load_u16(rom, index + 1)
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R16.DE, imm16])
        # LD (DE), A
        case 0x12:
            decoded = insn.Insn(
                name=insn.InsnName.LD,
                operands=[insn.IndirectR16(insn.R16.DE), insn.R8.A],
            )
        # LD D, n
        case 0x16:
            size = 2
            imm = rom[index + 1]
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R8.D, insn.U8(imm)]
            )
        # RLA
        case 0x17:
            decoded = insn.Insn(name=insn.InsnName.RLA)
        # LD A, (DE)
        case 0x1A:
            decoded = insn.Insn(
                name=insn.InsnName.LD,
                operands=[insn.R8.A, insn.IndirectR16(insn.R16.DE)],
            )
        # LD E, n
        case 0x1E:
            size = 2
            imm = rom[index + 1]
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R8.E, insn.U8(imm)]
            )
        # RRA
        case 0x1F:
            decoded = insn.Insn(name=insn.InsnName.RRA)
        # LD HL, nn
        case 0x21:
            size = 3
            imm16 = load_u16(rom, index + 1)
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R16.HL, imm16])
        # LD [HL+], A
        case 0x22:
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.IndirectHLIncr(), insn.R8.A]
            )
        # LD H, n
        case 0x26:
            size = 2
            imm = rom[index + 1]
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R8.H, insn.U8(imm)]
            )
        # DAA
        case 0x27:
            decoded = insn.Insn(name=insn.InsnName.DAA)
        # LD A, [HL+]
        case 0x2A:
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R8.A, insn.IndirectHLIncr()]
            )
        # LD L, n
        case 0x2E:
            size = 2
            imm = rom[index + 1]
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R8.L, insn.U8(imm)]
            )
        # CPL
        case 0x2F:
            decoded = insn.Insn(name=insn.InsnName.CPL)
        # LD SP, nn
        case 0x31:
            size = 3
            imm16 = load_u16(rom, index + 1)
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R16.SP, imm16])
        # LD [HL-], A
        case 0x32:
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.IndirectHLDecr(), insn.R8.A]
            )
        # LD [HL], n
        case 0x36:
            size = 2
            imm = rom[index + 1]
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R8.HL, insn.U8(imm)]
            )
        # SCF
        case 0x37:
            decoded = insn.Insn(name=insn.InsnName.SCF)
        # LD A, [HL-]
        case 0x3A:
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R8.A, insn.IndirectHLDecr()]
            )
        # CCF
        case 0x3F:
            decoded = insn.Insn(name=insn.InsnName.CCF)
        # LD A, n
        case 0x3E:
            size = 2
            imm = rom[index + 1]
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R8.A, insn.U8(imm)]
            )
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
        case 0x4A:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.D])
        # LD C, E
        case 0x4B:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.E])
        # LD C, H
        case 0x4C:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.H])
        # LD C, L
        case 0x4D:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.L])
        # LD C, [HL]
        case 0x4E:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.C, insn.R8.HL])
        # LD C, A
        case 0x4F:
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
        case 0x5A:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.D])
        # LD E, E
        case 0x5B:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.E])
        # LD E, H
        case 0x5C:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.H])
        # LD E, L
        case 0x5D:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.L])
        # LD E, [HL]
        case 0x5E:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.E, insn.R8.HL])
        # LD E, A
        case 0x5F:
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
        case 0x6A:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.D])
        # LD L, E
        case 0x6B:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.E])
        # LD L, H
        case 0x6C:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.H])
        # LD L, L
        case 0x6D:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.L])
        # LD L, [HL]
        case 0x6E:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.L, insn.R8.HL])
        # LD L, A
        case 0x6F:
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
        # HALT
        case 0x76:
            decoded = insn.Insn(name=insn.InsnName.HALT)
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
        case 0x7A:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.D])
        # LD A, E
        case 0x7B:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.E])
        # LD A, H
        case 0x7C:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.H])
        # LD A, L
        case 0x7D:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.L])
        # LD A, [HL]
        case 0x7E:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.HL])
        # LD A, A
        case 0x7F:
            decoded = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.A])
        # ADD B
        case 0x80:
            decoded = insn.Insn(name=insn.InsnName.ADD, operands=[insn.R8.B])
        # ADD C
        case 0x81:
            decoded = insn.Insn(name=insn.InsnName.ADD, operands=[insn.R8.C])
        # ADD D
        case 0x82:
            decoded = insn.Insn(name=insn.InsnName.ADD, operands=[insn.R8.D])
        # ADD E
        case 0x83:
            decoded = insn.Insn(name=insn.InsnName.ADD, operands=[insn.R8.E])
        # ADD H
        case 0x84:
            decoded = insn.Insn(name=insn.InsnName.ADD, operands=[insn.R8.H])
        # ADD L
        case 0x85:
            decoded = insn.Insn(name=insn.InsnName.ADD, operands=[insn.R8.L])
        # ADD (HL)
        case 0x86:
            decoded = insn.Insn(name=insn.InsnName.ADD, operands=[insn.R8.HL])
        # ADD A
        case 0x87:
            decoded = insn.Insn(name=insn.InsnName.ADD, operands=[insn.R8.A])
        # ADC B
        case 0x88:
            decoded = insn.Insn(name=insn.InsnName.ADC, operands=[insn.R8.B])
        # ADC C
        case 0x89:
            decoded = insn.Insn(name=insn.InsnName.ADC, operands=[insn.R8.C])
        # ADC D
        case 0x8A:
            decoded = insn.Insn(name=insn.InsnName.ADC, operands=[insn.R8.D])
        # ADC E
        case 0x8B:
            decoded = insn.Insn(name=insn.InsnName.ADC, operands=[insn.R8.E])
        # ADC H
        case 0x8C:
            decoded = insn.Insn(name=insn.InsnName.ADC, operands=[insn.R8.H])
        # ADC L
        case 0x8D:
            decoded = insn.Insn(name=insn.InsnName.ADC, operands=[insn.R8.L])
        # ADC (HL)
        case 0x8E:
            decoded = insn.Insn(name=insn.InsnName.ADC, operands=[insn.R8.HL])
        # ADC A
        case 0x8F:
            decoded = insn.Insn(name=insn.InsnName.ADC, operands=[insn.R8.A])
        # SUB B
        case 0x90:
            decoded = insn.Insn(name=insn.InsnName.SUB, operands=[insn.R8.B])
        # SUB C
        case 0x91:
            decoded = insn.Insn(name=insn.InsnName.SUB, operands=[insn.R8.C])
        # SUB D
        case 0x92:
            decoded = insn.Insn(name=insn.InsnName.SUB, operands=[insn.R8.D])
        # SUB E
        case 0x93:
            decoded = insn.Insn(name=insn.InsnName.SUB, operands=[insn.R8.E])
        # SUB H
        case 0x94:
            decoded = insn.Insn(name=insn.InsnName.SUB, operands=[insn.R8.H])
        # SUB L
        case 0x95:
            decoded = insn.Insn(name=insn.InsnName.SUB, operands=[insn.R8.L])
        # SUB (HL)
        case 0x96:
            decoded = insn.Insn(name=insn.InsnName.SUB, operands=[insn.R8.HL])
        # SUB A
        case 0x97:
            decoded = insn.Insn(name=insn.InsnName.SUB, operands=[insn.R8.A])
        # SBC B
        case 0x98:
            decoded = insn.Insn(name=insn.InsnName.SBC, operands=[insn.R8.B])
        # SBC C
        case 0x99:
            decoded = insn.Insn(name=insn.InsnName.SBC, operands=[insn.R8.C])
        # SBC D
        case 0x9A:
            decoded = insn.Insn(name=insn.InsnName.SBC, operands=[insn.R8.D])
        # SBC E
        case 0x9B:
            decoded = insn.Insn(name=insn.InsnName.SBC, operands=[insn.R8.E])
        # SBC H
        case 0x9C:
            decoded = insn.Insn(name=insn.InsnName.SBC, operands=[insn.R8.H])
        # SBC L
        case 0x9D:
            decoded = insn.Insn(name=insn.InsnName.SBC, operands=[insn.R8.L])
        # SBC (HL)
        case 0x9E:
            decoded = insn.Insn(name=insn.InsnName.SBC, operands=[insn.R8.HL])
        # SBC A
        case 0x9F:
            decoded = insn.Insn(name=insn.InsnName.SBC, operands=[insn.R8.A])
        # AND B
        case 0xA0:
            decoded = insn.Insn(name=insn.InsnName.AND, operands=[insn.R8.B])
        # AND C
        case 0xA1:
            decoded = insn.Insn(name=insn.InsnName.AND, operands=[insn.R8.C])
        # AND D
        case 0xA2:
            decoded = insn.Insn(name=insn.InsnName.AND, operands=[insn.R8.D])
        # AND E
        case 0xA3:
            decoded = insn.Insn(name=insn.InsnName.AND, operands=[insn.R8.E])
        # AND H
        case 0xA4:
            decoded = insn.Insn(name=insn.InsnName.AND, operands=[insn.R8.H])
        # AND L
        case 0xA5:
            decoded = insn.Insn(name=insn.InsnName.AND, operands=[insn.R8.L])
        # AND (HL)
        case 0xA6:
            decoded = insn.Insn(name=insn.InsnName.AND, operands=[insn.R8.HL])
        # AND A
        case 0xA7:
            decoded = insn.Insn(name=insn.InsnName.AND, operands=[insn.R8.A])
        # XOR B
        case 0xA8:
            decoded = insn.Insn(name=insn.InsnName.XOR, operands=[insn.R8.B])
        # XOR C
        case 0xA9:
            decoded = insn.Insn(name=insn.InsnName.XOR, operands=[insn.R8.C])
        # XOR D
        case 0xAA:
            decoded = insn.Insn(name=insn.InsnName.XOR, operands=[insn.R8.D])
        # XOR E
        case 0xAB:
            decoded = insn.Insn(name=insn.InsnName.XOR, operands=[insn.R8.E])
        # XOR H
        case 0xAC:
            decoded = insn.Insn(name=insn.InsnName.XOR, operands=[insn.R8.H])
        # XOR L
        case 0xAD:
            decoded = insn.Insn(name=insn.InsnName.XOR, operands=[insn.R8.L])
        # XOR (HL)
        case 0xAE:
            decoded = insn.Insn(name=insn.InsnName.XOR, operands=[insn.R8.HL])
        # XOR A
        case 0xAF:
            decoded = insn.Insn(name=insn.InsnName.XOR, operands=[insn.R8.A])
        # OR B
        case 0xB0:
            decoded = insn.Insn(name=insn.InsnName.OR, operands=[insn.R8.B])
        # OR C
        case 0xB1:
            decoded = insn.Insn(name=insn.InsnName.OR, operands=[insn.R8.C])
        # OR D
        case 0xB2:
            decoded = insn.Insn(name=insn.InsnName.OR, operands=[insn.R8.D])
        # OR E
        case 0xB3:
            decoded = insn.Insn(name=insn.InsnName.OR, operands=[insn.R8.E])
        # OR H
        case 0xB4:
            decoded = insn.Insn(name=insn.InsnName.OR, operands=[insn.R8.H])
        # OR L
        case 0xB5:
            decoded = insn.Insn(name=insn.InsnName.OR, operands=[insn.R8.L])
        # OR (HL)
        case 0xB6:
            decoded = insn.Insn(name=insn.InsnName.OR, operands=[insn.R8.HL])
        # OR A
        case 0xB7:
            decoded = insn.Insn(name=insn.InsnName.OR, operands=[insn.R8.A])
        # CP B
        case 0xB8:
            decoded = insn.Insn(name=insn.InsnName.CP, operands=[insn.R8.B])
        # CP C
        case 0xB9:
            decoded = insn.Insn(name=insn.InsnName.CP, operands=[insn.R8.C])
        # CP D
        case 0xBA:
            decoded = insn.Insn(name=insn.InsnName.CP, operands=[insn.R8.D])
        # CP E
        case 0xBB:
            decoded = insn.Insn(name=insn.InsnName.CP, operands=[insn.R8.E])
        # CP H
        case 0xBC:
            decoded = insn.Insn(name=insn.InsnName.CP, operands=[insn.R8.H])
        # CP L
        case 0xBD:
            decoded = insn.Insn(name=insn.InsnName.CP, operands=[insn.R8.L])
        # CP (HL)
        case 0xBE:
            decoded = insn.Insn(name=insn.InsnName.CP, operands=[insn.R8.HL])
        # CP A
        case 0xBF:
            decoded = insn.Insn(name=insn.InsnName.CP, operands=[insn.R8.A])
        # POP BC
        case 0xC1:
            decoded = insn.Insn(name=insn.InsnName.POP, operands=[insn.R16.BC])
        # PUSH BC
        case 0xC5:
            decoded = insn.Insn(name=insn.InsnName.PUSH, operands=[insn.R16.BC])
        # POP DE
        case 0xD1:
            decoded = insn.Insn(name=insn.InsnName.POP, operands=[insn.R16.DE])
        # PUSH BC
        case 0xD5:
            decoded = insn.Insn(name=insn.InsnName.PUSH, operands=[insn.R16.DE])
        # LDH [n], A
        case 0xE0:
            size = 2
            offset = rom[index + 1]
            decoded = insn.Insn(
                name=insn.InsnName.LDH,
                operands=[insn.DirectU16(insn.U16(0xFF00 + offset)), insn.R8.A],
            )
        # POP HL
        case 0xE1:
            decoded = insn.Insn(name=insn.InsnName.POP, operands=[insn.R16.HL])
        # LDH (C), A
        case 0xE2:
            decoded = insn.Insn(
                name=insn.InsnName.LDH, operands=[insn.IndirectHramC(), insn.R8.A]
            )
        # PUSH HL
        case 0xE5:
            decoded = insn.Insn(name=insn.InsnName.PUSH, operands=[insn.R16.HL])
        # LD [nn], A
        case 0xEA:
            size = 3
            addr = load_u16(rom, index + 1)
            decoded = insn.Insn(
                name=insn.InsnName.LD,
                operands=[insn.DirectU16(addr), insn.R8.A],
            )
        # LDH A, [n]
        case 0xF0:
            size = 2
            offset = rom[index + 1]
            decoded = insn.Insn(
                name=insn.InsnName.LDH,
                operands=[insn.R8.A, insn.DirectU16(insn.U16(0xFF00 + offset))],
            )
        # POP AF
        case 0xF1:
            decoded = insn.Insn(name=insn.InsnName.POP, operands=[insn.R16.AF])
        # LDH A, [C]
        case 0xF2:
            decoded = insn.Insn(
                name=insn.InsnName.LDH, operands=[insn.R8.A, insn.IndirectHramC()]
            )
        # DI
        case 0xF3:
            decoded = insn.Insn(name=insn.InsnName.DI)
        # PUSH AF
        case 0xF5:
            decoded = insn.Insn(name=insn.InsnName.PUSH, operands=[insn.R16.AF])
        # LD SP, HL
        case 0xF9:
            decoded = insn.Insn(
                name=insn.InsnName.LD, operands=[insn.R16.SP, insn.R16.HL]
            )
        # LD A, [nn]
        case 0xFA:
            size = 3
            addr = load_u16(rom, index + 1)
            decoded = insn.Insn(
                name=insn.InsnName.LD,
                operands=[insn.R8.A, insn.DirectU16(addr)],
            )
        # EI
        case 0xFB:
            decoded = insn.Insn(name=insn.InsnName.EI)

    return DecodedInsn(insn=decoded, size=size) if decoded is not None else None


def load_u16(rom: bytes, index: int) -> insn.U16:
    """Reads an unsigned 16-bit value in little endian order"""
    return insn.U16(rom[index] + (rom[index + 1] << 8))
