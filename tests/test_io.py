import pathlib
import tempfile

from charybdis import io


def test_create_output_directory() -> None:
    with tempfile.TemporaryDirectory() as dir:
        output_directory_path = pathlib.Path(f"{dir}/output")
        created = io.create_output_directory(
            io.DisassemblerState(
                output_directory_path=output_directory_path,
                overwrite=False,
                rom_data=bytes(),
                rom_ext="",
                rom_file_path=pathlib.Path("/"),
                rom_md5="",
            )
        )
    assert created


def test_create_output_directory__exists() -> None:
    with tempfile.TemporaryDirectory() as dir:
        created = io.create_output_directory(
            io.DisassemblerState(
                output_directory_path=pathlib.Path(dir),
                overwrite=False,
                rom_data=bytes(),
                rom_ext="",
                rom_file_path=pathlib.Path("/"),
                rom_md5="",
            )
        )
    assert not created


def test_create_output_directory__overwrite() -> None:
    with tempfile.TemporaryDirectory() as dir:
        created = io.create_output_directory(
            io.DisassemblerState(
                output_directory_path=pathlib.Path(dir),
                overwrite=True,
                rom_data=bytes(),
                rom_ext="",
                rom_file_path=pathlib.Path("/"),
                rom_md5="",
            )
        )
    assert created
