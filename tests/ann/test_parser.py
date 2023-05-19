import os
import tempfile

import pytest

from charybdis.ann import parser, types


def test_parse_ann__untyped() -> None:
    assert types.ann(0x01, 0x1234, "Test") == parser.parse_ann("01:1234 Test")


TYPE_TEST_CASES = [
    (types.PrimitiveType.U8, "u8"),
    (types.PrimitiveType.U16, "u16"),
    (types.ArrayType(type=types.PrimitiveType.U8, size=5), "[5]u8"),
    (types.PointerType(type=types.PrimitiveType.U8), "*u8"),
    (
        types.ArrayType(type=types.PointerType(type=types.PrimitiveType.U8), size=16),
        "[0x10]*u8",
    ),
]


@pytest.mark.parametrize("type,type_str", TYPE_TEST_CASES)
def test_parse_ann__typed(type: types.AnnType, type_str: str) -> None:
    ann = types.ann(0x01, 0x1234, "A", type)
    assert ann == parser.parse_ann(f"01:1234 A, {type_str}")


ANN_FILE = """
01:1234 Test, u8
ff:beef Beef, [5]u16
""".strip()


def test_parse_ann_file() -> None:
    anns = [
        types.ann(0x01, 0x1234, "Test", types.PrimitiveType.U8),
        types.ann(
            0xFF, 0xBEEF, "Beef", types.ArrayType(type=types.PrimitiveType.U16, size=5)
        ),
    ]
    with tempfile.TemporaryFile(mode="w+") as f:
        f.write(ANN_FILE)
        f.seek(0, os.SEEK_SET)
        assert anns == parser.parse_ann_file(f)
