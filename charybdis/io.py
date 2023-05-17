import dataclasses
import hashlib
import logging
import os.path
import pathlib
import shutil
import typing
from typing import Any, TypedDict

import chevron

from charybdis import disasm

FILE_CHUNK_SIZE = 1024  # 1 KB
MAKEFILE_TEMPLATE_PATH = pathlib.Path("templates/Makefile.mustache")

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DisassemblerOptions:
    output_directory_path: pathlib.Path
    rom_file_path: pathlib.Path
    overwrite: bool


class MakefileData(TypedDict):
    rom_md5: str
    rom_ext: str


@dataclasses.dataclass
class DisassemblerState(DisassemblerOptions):
    rom_data: bytes
    rom_md5: str
    rom_ext: str


def disassemble(options: DisassemblerOptions) -> None:
    state = initialize_state(options)
    create_output_directory(state)
    write_assembly(state)
    write_makefile(state)


def initialize_state(options: DisassemblerOptions) -> DisassemblerState:
    rom_data = bytearray()
    rom_md5 = hashlib.md5()
    with open(options.rom_file_path, "rb") as f:
        done = False
        while not done:
            chunk = f.read(FILE_CHUNK_SIZE)
            rom_data.extend(chunk)
            rom_md5.update(chunk)
            done = len(chunk) < FILE_CHUNK_SIZE
    return DisassemblerState(
        **dataclasses.asdict(options),
        rom_data=bytes(rom_data),
        rom_md5=rom_md5.hexdigest(),
        # TODO: Use ROM header instead of file extension
        rom_ext=options.rom_file_path.suffix,
    )


def create_output_directory(state: DisassemblerState) -> bool:
    if os.path.exists(state.output_directory_path):
        if not state.overwrite:
            logging.warning("output directory exists but overwrite not enabled")
            return False
        shutil.rmtree(state.output_directory_path)
    state.output_directory_path.mkdir(parents=True, exist_ok=False)
    return True


def write_assembly(state: DisassemblerState) -> None:
    # TODO: Refactor
    with open(state.output_directory_path / "game.asm", "w") as f:
        i = 0
        while i < len(state.rom_data):
            if i % 0x4000 == 0:
                bank = i // 0x4000
                start = 0
                type = "ROM0"
                options = ""
                if i != 0:
                    start = 0x4000
                    type = "ROMX"
                    options = f", BANK[${bank:x}]"
                f.write(
                    f'SECTION "ROM Bank ${bank:03x}", {type}[${start:x}]{options}\n\n'
                )
            result = disasm.decode_insn(state.rom_data, i)
            if result is not None:
                size = result.size
                f.write(f"{result.insn.render()}\n")
            else:
                size = 1
                f.write(f"DB ${state.rom_data[i]:02x}\n")
            # NB: Shouldn't write something that spans multiple banks
            assert (i % 0x4000) < ((i + size) % 0x4000) or size == 1
            i += size


def write_makefile(state: DisassemblerState) -> None:
    makefile_path = state.output_directory_path / "Makefile"
    with open(MAKEFILE_TEMPLATE_PATH, "r") as f:
        # NB: TypedDict is not a subtype of dict[str, Any] so cast
        #     https://github.com/python/mypy/issues/4976
        makefile_data = {"rom_ext": state.rom_ext, "rom_md5": state.rom_md5}
        data = typing.cast(dict[str, Any], makefile_data)
        makefile = chevron.render(f, data)
    with open(makefile_path, "w") as f:
        f.write(makefile)
