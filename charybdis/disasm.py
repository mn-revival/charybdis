import dataclasses
import hashlib
import logging
import os.path
import pathlib
import shutil
import typing
from typing import Any, TypedDict

import chevron

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

    @property
    def makefile_data(self) -> MakefileData:
        return {"rom_ext": self.rom_ext, "rom_md5": self.rom_md5}


def disassemble(options: DisassemblerOptions) -> None:
    state = initialize_state(options)
    create_output_directory(state)
    # TODO: Populate file with data
    with open(state.output_directory_path / "game.asm", "w") as f:
        pass
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
    state = DisassemblerState(
        **dataclasses.asdict(options),
        rom_data=bytes(rom_data),
        rom_md5=rom_md5.hexdigest(),
        # TODO: Use ROM header instead of file extension
        rom_ext=options.rom_file_path.suffix,
    )
    return state


def create_output_directory(state: DisassemblerState) -> bool:
    if os.path.exists(state.output_directory_path):
        if not state.overwrite:
            logging.warn("output directory exists but overwrite not enabled")
            return False
        shutil.rmtree(state.output_directory_path)
    state.output_directory_path.mkdir(parents=True, exist_ok=False)
    return True


def write_makefile(state: DisassemblerState) -> None:
    makefile_path = state.output_directory_path / "Makefile"
    with open(MAKEFILE_TEMPLATE_PATH, "r") as f:
        # NB: TypedDict is not a subtype of dict[str, Any] so cast
        #     https://github.com/python/mypy/issues/4976
        data = typing.cast(dict[str, Any], state.makefile_data)
        makefile = chevron.render(f, data)
    with open(makefile_path, "w") as f:
        f.write(makefile)
