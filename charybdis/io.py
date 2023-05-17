import dataclasses
import hashlib
import logging
import os.path
import pathlib
import shutil
import typing
from typing import Any, TextIO, TypedDict

import chevron

from charybdis import disasm

ROM_BANK_SIZE = 0x4000  # 16 KiB
ROM0_BANK_START = 0
ROMX_BANK_START = 0x4000

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
    # TODO: Use ROM header instead of file length
    num_banks = len(state.rom_data) // 0x4000
    for bank in range(num_banks):
        with open(state.output_directory_path / f"bank_{bank:03x}.asm", "w") as f:
            write_bank(state, f, bank)


def get_bank_header(bank: int) -> str:
    start = ROM0_BANK_START
    type = "ROM0"
    options = ""
    if bank != 0:
        start = ROMX_BANK_START
        type = "ROMX"
        options = f", BANK[${bank:x}]"
    return f'SECTION "ROM Bank ${bank:03x}", {type}[${start:x}]{options}\n\n'


def write_bank(state: DisassemblerState, f: TextIO, bank: int) -> None:
    f.write(get_bank_header(bank))
    offset = 0
    while offset < ROM_BANK_SIZE:
        index = ROM_BANK_SIZE * bank + offset
        result = disasm.decode_insn(state.rom_data, index)
        if result is not None:
            size = result.size
            line = result.insn.render()
        else:
            size = 1
            line = f"DB ${state.rom_data[index]:02x}"
        f.write(line)
        f.write("\n")
        # NB: Shouldn't write something that spans multiple banks
        assert (offset % ROM_BANK_SIZE) < ((offset + size) % ROM_BANK_SIZE) or size == 1
        offset += size


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
