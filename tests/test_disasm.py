from typing import Iterable, List, Union

import pytest
import subprocess

from charybdis import disasm, insn

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

ALU_ORDER = [
    insn.InsnName.ADD,
    insn.InsnName.ADC,
    insn.InsnName.SUB,
    insn.InsnName.SBC,
    insn.InsnName.AND,
    insn.InsnName.XOR,
    insn.InsnName.OR,
    insn.InsnName.CP,
]

CB_R8_ORDER = [
    insn.InsnName.RLC,
    insn.InsnName.RRC,
    insn.InsnName.RL,
    insn.InsnName.RR,
    insn.InsnName.SLA,
    insn.InsnName.SRA,
    insn.InsnName.SWAP,
    insn.InsnName.SRL,
]

CB_U3_R8_ORDER = [
    insn.InsnName.BIT,
    insn.InsnName.RES,
    insn.InsnName.SET,
]


def _assert_decode(data: Iterable[int], expected: insn.Insn) -> None:
    data_bytes = bytes(data)
    result = disasm.decode_insn(data_bytes, 0)
    assert result is not None
    assert len(data_bytes) == result.size
    assert expected == result.insn


NULLARY_CASES = [
    (insn.InsnName.NOP, [0x00]),
    (insn.InsnName.RLCA, [0x07]),
    (insn.InsnName.RRCA, [0x0F]),
    (insn.InsnName.RLA, [0x17]),
    (insn.InsnName.RRA, [0x1F]),
    (insn.InsnName.DAA, [0x27]),
    (insn.InsnName.CPL, [0x2F]),
    (insn.InsnName.SCF, [0x37]),
    (insn.InsnName.CCF, [0x3F]),
    (insn.InsnName.HALT, [0x76]),
    (insn.InsnName.DI, [0xF3]),
    (insn.InsnName.EI, [0xFB]),
]


@pytest.mark.parametrize("name,data", NULLARY_CASES)
@pytest.mark.skip(reason="not implemented")
def test_decode_insn__nullary(name: insn.InsnName, data: Iterable[int]) -> None:
    _assert_decode(bytes(data), insn.Insn(name=name))


LD_R_R_CASES = [
    (insn.InsnName.LD, r1, r2, 0x40 + 8 * y + x)
    for x, r2 in enumerate(R8_ORDER)
    for y, r1 in enumerate(R8_ORDER)
    if not (r1 == insn.R8.HL and r2 == r1)
]


@pytest.mark.parametrize("name,r1,r2,byte", LD_R_R_CASES)
def test_decode_insn__r8_r8(
    name: insn.InsnName, r1: insn.R8, r2: insn.R8, byte: int
) -> None:
    _assert_decode([byte], insn.Insn(name=name, operands=[r1, r2]))


ALU_R8_CASES = [
    (name, r, [0x80 + 8 * y + x])
    for x, r in enumerate(R8_ORDER)
    for y, name in enumerate(ALU_ORDER)
]

CB_R8_CASES = [
    (name, r, [0xCB, 8 * y + x])
    for x, r in enumerate(R8_ORDER)
    for y, name in enumerate(CB_R8_ORDER)
]


@pytest.mark.parametrize("name,r,data", ALU_R8_CASES + CB_R8_CASES)
@pytest.mark.skip(reason="not implemented")
def test_decode_insn__r8(name: insn.InsnName, r: insn.R8, data: Iterable[int]) -> None:
    _assert_decode(data, insn.Insn(name=name, operands=[r]))


U3_R8_CASES = [
    (name, bit, r, [0xCB, 0x40 * y + 0x40 + 8 * bit + x])
    for x, r in enumerate(R8_ORDER)
    for bit in range(8)
    for y, name in enumerate(CB_U3_R8_ORDER)
]


@pytest.mark.parametrize("name,bit,r,data", U3_R8_CASES)
@pytest.mark.skip(reason="not implemented")
def test_decode_insn__u3_r8(
    name: insn.InsnName, bit: int, r: insn.R8, data: Iterable[int]
) -> None:
    _assert_decode(data, insn.Insn(name=name, operands=[insn.U3(bit), r]))


def test_disassembly_correspondence() -> None:
    section_name = "ROM Bank $000"

    def disassemble(code: bytes) -> str:
        offset = 0
        text = ""
        while offset < len(code):
            result = disasm.decode_insn(code, offset)
            assert result is not None
            text += result.insn.render()
            text += "\n"
            offset += result.size
        header = f'SECTION "{section_name}", ROM0[$150]\n'
        return header + text

    def assemble(asm: str) -> bytes:
        process = subprocess.Popen(
            [
                "docker",
                "run",
                "--rm",
                "-i",
                "rgbds",
                "rgbasm",
                "-o",
                "/dev/stdout",
                "-",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        assert process.stdin is not None
        assert process.stdout is not None

        process.stdin.write(asm.encode("utf-8"))
        process.stdin.close()

        obj: bytes = process.stdout.read()

        # Section size is located 0x14 (length of headers) + length of name + 1 (null terminator)
        size_index = 0x14 + len(section_name) + 1
        section_size = (
            obj[size_index]
            + (obj[size_index + 1] << 8)
            + (obj[size_index + 2] << 16)
            + (obj[size_index + 3] << 24)
        )

        code_index = size_index + 18

        return obj[code_index : (code_index + section_size)]

    with open("tests/test.asm", "r") as f:
        asm = f.read()
        code = assemble(asm)
        asm_2 = disassemble(code)
        code_2 = assemble(asm_2)

        assert code == code_2
