import hashlib
import io as python_io
import pathlib
import tempfile

from charybdis import io


def test_create_output_directory() -> None:
    with tempfile.TemporaryDirectory() as dir:
        created = io.create_output_directory(_create_state(f"{dir}/output"))
    assert created


def test_create_output_directory__exists() -> None:
    with tempfile.TemporaryDirectory() as dir:
        created = io.create_output_directory(_create_state(dir))
    assert not created


def test_create_output_directory__overwrite() -> None:
    with tempfile.TemporaryDirectory() as dir:
        created = io.create_output_directory(_create_state(dir, overwrite=True))
    assert created


def test_write_makefile() -> None:
    rom_md5 = hashlib.md5().hexdigest()
    with tempfile.TemporaryDirectory() as dir:
        io.write_makefile(_create_state(dir, rom_md5=rom_md5))
        makefile_path = pathlib.Path(dir) / "Makefile"
        assert makefile_path.exists()
        assert makefile_path.is_file()


def test_get_bank_header() -> None:
    assert 'SECTION "ROM Bank $000", ROM0[$0]' == io.get_bank_header(0)
    assert 'SECTION "ROM Bank $101", ROMX[$4000], BANK[$101]' == io.get_bank_header(
        0x101
    )


NOP_ASM = "nop\n" * io.ROM_BANK_SIZE
BANK_ASM = f"""SECTION "ROM Bank $000", ROM0[$0]

{NOP_ASM}"""


def test_write_bank() -> None:
    state = _create_state(".")
    state.rom_data = bytes([0x00 for _ in range(io.ROM_BANK_SIZE)])
    buffer = python_io.StringIO()
    io.write_bank(state, buffer, 0)
    assert BANK_ASM == buffer.getvalue()


def _create_state(
    dir: str, overwrite: bool = False, rom_md5: str = ""
) -> io.DisassemblerState:
    return io.DisassemblerState(
        anns=[],
        is_gbc=False,
        output_directory_path=pathlib.Path(dir),
        overwrite=overwrite,
        rom_banks=2,
        rom_data=bytes(),
        rom_file_path=pathlib.Path("/"),
        rom_md5=rom_md5,
    )
