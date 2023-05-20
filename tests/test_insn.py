from charybdis import insn

import pytest


def test_insn__render() -> None:
    ld = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.B])
    assert "ld a, b" == ld.render()


def test_insn__render__no_operands() -> None:
    ret = insn.Insn(name=insn.InsnName.RET)
    assert "ret" == ret.render()


@pytest.mark.parametrize(
    "insn_str,_insn",
    [
        ("main", insn.Label("main")),
        ("a", insn.R8.A),
        ("[hl]", insn.R8.HL),
        ("hl", insn.R16.HL),
        ("5", insn.U3(0x5)),
        ("$ff", insn.U8(0xFF)),
        ("$abcd", insn.U16(0xABCD)),
        ("[$abcd]", insn.DirectU16(0xABCD)),
        ("[c]", insn.IndirectHramC()),
        ("[bc]", insn.IndirectR16(insn.R16.BC)),
        ("[hl+]", insn.IndirectHLIncr()),
        ("[hl-]", insn.IndirectHLDecr()),
    ],
)
def test_render_operand(insn_str: str, _insn: insn.Insn) -> None:
    assert insn_str == insn.render_operand(_insn)


def test_render_operand__unsupported() -> None:
    with pytest.raises(Exception):
        insn.render_operand("Unsupported raw string")
