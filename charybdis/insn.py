import dataclasses
import enum


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


# TODO: Union with richer types
InsnOperand = str


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
            operands = " " + ", ".join(self.operands)
        return f"{name}{operands}"
