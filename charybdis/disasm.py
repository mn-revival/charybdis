import dataclasses


@dataclasses.dataclass
class DisassemblerOptions:
    output_directory_path: str
    rom_file_path: str


def disassemble(options: DisassemblerOptions) -> None:
    pass
