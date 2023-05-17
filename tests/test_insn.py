from charybdis import insn


def test_insn__render() -> None:
    ld = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.B])
    assert "ld a, b" == ld.render()


def test_insn__render__no_operands() -> None:
    ret = insn.Insn(name=insn.InsnName.RET)
    assert "ret" == ret.render()


def test_render_operand__r8() -> None:
    assert "a" == insn.render_operand(insn.R8.A)
    assert "[hl]" == insn.render_operand(insn.R8.HL)


def test_render_operand__r16() -> None:
    assert "hl" == insn.render_operand(insn.R16.HL)


def test_render_operand__imm() -> None:
    assert "$ff" == insn.render_operand(insn.U8(0xFF))
    assert "$ffff" == insn.render_operand(insn.U16(0xFFFF))


def test_render_operand__label() -> None:
    assert "main" == insn.render_operand(insn.Label("main"))
