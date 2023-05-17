import dataclasses
import logging
import os.path
import pathlib
import shutil


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DisassemblerOptions:
    output_directory_path: pathlib.Path
    rom_file_path: pathlib.Path
    overwrite: bool = dataclasses.field(default=False)


def disassemble(options: DisassemblerOptions) -> None:
    if os.path.exists(options.output_directory_path):
        if not options.overwrite:
            logging.warn("output directory exists but overwrite not enabled")
            return
        shutil.rmtree(options.output_directory_path)
    options.output_directory_path.mkdir(parents=True, exist_ok=False)
