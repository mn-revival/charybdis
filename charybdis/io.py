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
from charybdis.ann import parser, types as ann_types

OFFSET_CGB_FLAG = 0x0143
OFFSET_ROM_SIZE = 0x0148

ROM_BANK_SIZE = 0x4000  # 16 KiB
ROM0_BANK_START = 0
ROMX_BANK_START = 0x4000

EXTENSION_GB = ".gb"
EXTENSION_GBC = ".gbc"

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
    anns: list[ann_types.Ann]
    rom_banks: int
    rom_data: bytes
    rom_md5: str
    is_gbc: bool


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
    anns = []
    ann_file_path = options.rom_file_path.with_suffix(".ann")
    if ann_file_path.exists() and ann_file_path.is_file():
        logging.info("annotation file exists, parsing")
        with open(ann_file_path, "r") as f:
            anns = parser.parse_ann_file(f)
    return DisassemblerState(
        **dataclasses.asdict(options),
        anns=anns,
        is_gbc=(rom_data[OFFSET_CGB_FLAG] & 0x80) > 0,
        rom_banks=2 << rom_data[OFFSET_ROM_SIZE],
        rom_data=bytes(rom_data),
        rom_md5=rom_md5.hexdigest(),
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
    for bank in range(state.rom_banks):
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
        makefile_data = {
            "rom_ext": EXTENSION_GBC if state.is_gbc else EXTENSION_GB,
            "rom_md5": state.rom_md5,
        }
        data = typing.cast(dict[str, Any], makefile_data)
        makefile = chevron.render(f, data)
    with open(makefile_path, "w") as f:
        f.write(makefile)
