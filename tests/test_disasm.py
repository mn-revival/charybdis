from charybdis import disasm, insn


def test_decode_insn__nop() -> None:
    result = disasm.decode_insn(bytes([0x00]), 0)
    assert result is not None
    assert result.size == 1
    assert result.insn == insn.Insn(name=insn.InsnName.NOP)
