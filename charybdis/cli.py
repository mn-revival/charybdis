import argparse
import pathlib

from charybdis import io


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--overwrite", action=argparse.BooleanOptionalAction)
    parser.add_argument("rom_file_path", metavar="rom.gb")
    parser.add_argument(
        "output_directory_path", metavar="output_dir", default="output", nargs="?"
    )
    return parser


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()
    io.disassemble(
        io.DisassemblerOptions(
            output_directory_path=pathlib.Path(args.output_directory_path),
            overwrite=args.overwrite,
            rom_file_path=pathlib.Path(args.rom_file_path),
        )
    )


if __name__ == "__main__":
    main()
