import argparse

from charybdis import disasm


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("rom_file_path", metavar="rom.gb")
    parser.add_argument("output_directory_path", metavar="output_dir")
    return parser


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    disasm.disassemble(
        disasm.DisassemblerOptions(
            output_directory_path=args.output_directory_path,
            rom_file_path=args.rom_file_path,
        )
    )


if __name__ == "__main__":
    main()
