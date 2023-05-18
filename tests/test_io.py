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


def _create_state(dir: str, overwrite: bool = False) -> io.DisassemblerState:
    return io.DisassemblerState(
        is_gbc=False,
        output_directory_path=pathlib.Path(dir),
        overwrite=overwrite,
        rom_banks=2,
        rom_data=bytes(),
        rom_file_path=pathlib.Path("/"),
        rom_md5="",
    )
