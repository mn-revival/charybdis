import dataclasses
import enum
from typing import Union


class InsnName(enum.Enum):
    """All possible SM83 instruction names"""

    ADC = "ADC"
    ADD = "ADD"
    AND = "AND"
    BIT = "BIT"
    CALL = "CALL"
    CCF = "CCF"
    CP = "CP"
    CPL = "CPL"
    DAA = "DAA"
    DEC = "DEC"
    DI = "DI"
    EI = "EI"
    HALT = "HALT"
    INC = "INC"
    JP = "JP"
    JR = "JR"
    LD = "LD"
    LDH = "LDH"
    OR = "OR"
    NOP = "NOP"
    POP = "POP"
    PUSH = "PUSH"
    RES = "RES"
    RET = "RET"
    RETI = "RETI"
    RL = "RL"
    RLA = "RLA"
    RLC = "RLC"
    RLCA = "RLCA"
    RR = "RR"
    RRA = "RRA"
    RRC = "RRC"
    RRCA = "RRCA"
    RST = "RST"
    SBC = "SBC"
    SCF = "SCF"
    SET = "SET"
    SUB = "SUB"
    SLA = "SLA"
    SRA = "SRA"
    SRL = "SRL"
    STOP = "STOP"
    SWAP = "SWAP"
    XOR = "XOR"


# TODO: More we can do here (addressing modes, etc)
@dataclasses.dataclass
class Label:
    """Reference to a location or value"""

    value: str


@dataclasses.dataclass
class U3:
    """3-bit unsigned integer"""

    value: int


@dataclasses.dataclass
class U8:
    """8-bit unsigned integer"""

    value: int


@dataclasses.dataclass
class U16:
    """16-bit unsigned integer"""

    value: int


class R8(enum.Enum):
    """8-bit register"""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    H = "H"
    L = "L"
    HL = "[HL]"


class R16(enum.Enum):
    """16-bit register"""

    AF = "AF"
    BC = "BC"
    DE = "DE"
    HL = "HL"
    SP = "SP"


@dataclasses.dataclass
class DirectU16:
    """Direct addressing mode via 16-bit integer"""

    offset: U16


class IndirectHramC:
    """Indirect addressing of HRAM through register C"""


@dataclasses.dataclass
class IndirectR16:
    """Indirect addressing mode via 16-bit register"""

    reg: R16


@dataclasses.dataclass
class IndirectHLIncr:
    """Indirect addressing mode via HL with increment"""


@dataclasses.dataclass
class IndirectHLDecr:
    """Indirect addressing mode via HL with decrement"""


InsnOperand = Union[
    Label,
    R8,
    R16,
    U3,
    U8,
    U16,
    DirectU16,
    IndirectHramC,
    IndirectR16,
    IndirectHLIncr,
    IndirectHLDecr,
]


@dataclasses.dataclass
class Insn:
    """A single SM83 instruction"""

    name: InsnName
    operands: list[InsnOperand] = dataclasses.field(default_factory=list)

    def render(self) -> str:
        """Render to an RGBDS-compatible string representation"""
        name = self.name.value.lower()
        operands = ""
        if len(self.operands) > 0:
            operands = " " + ", ".join([render_operand(op) for op in self.operands])
        return f"{name}{operands}"


def render_operand(operand: InsnOperand) -> str:
    s = ""
    match operand:
        case Label(value):
            s = value
        case R8() | R16():
            s = operand.value.lower()
        case U3(value):
            s = str(value)
        case U8(value) | U16(value):
            s = f"${value:x}"
        case DirectU16(offset):
            s = f"[${offset:x}]"
        case IndirectHramC():
            s = "[c]"
        case IndirectR16(reg):
            s = f"[{render_operand(reg)}]"
        case IndirectHLIncr():
            s = "[hl+]"
        case IndirectHLDecr():
            s = "[hl-]"
        case _:
            raise Exception(f"unknown operand type: {type(operand)}")
    return s
