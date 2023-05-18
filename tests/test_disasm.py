import pytest

from charybdis import disasm, insn


def test_decode_insn__nop() -> None:
    result = disasm.decode_insn(bytes([0x00]), 0)
    assert result is not None
    assert 1 == result.size
    assert insn.Insn(name=insn.InsnName.NOP) == result.insn


R8_ORDER = [
    insn.R8.B,
    insn.R8.C,
    insn.R8.D,
    insn.R8.E,
    insn.R8.H,
    insn.R8.L,
    insn.R8.HL,
    insn.R8.A,
]

LD_R_R_CASES = [
    (r1, r2, 0x40 + 8 * R8_ORDER.index(r1) + i)
    for i, r2 in enumerate(R8_ORDER)
    for r1 in insn.R8
    if not (r1 == insn.R8.HL and r2 == r1)
]


@pytest.mark.parametrize("r1,r2,byte", LD_R_R_CASES)
def test_decode_insn__ld_r_r(r1: insn.R8, r2: insn.R8, byte: int) -> None:
    result = disasm.decode_insn(bytes([byte]), 0)
    assert result is not None
    assert 1 == result.size
    assert insn.Insn(name=insn.InsnName.LD, operands=[r1, r2]) == result.insn
