from charybdis import insn


def test_insn__render() -> None:
    ld = insn.Insn(name=insn.InsnName.LD, operands=[insn.R8.A, insn.R8.B])
    assert "ld a, b" == ld.render()


def test_insn__render__no_operands() -> None:
    ret = insn.Insn(name=insn.InsnName.RET)
    assert "ret" == ret.render()
