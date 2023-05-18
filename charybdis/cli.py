import argparse
import pathlib

from charybdis import io


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--overwrite",
        action=argparse.BooleanOptionalAction,
        help="do/don't overwrite output directory",
    )
    parser.add_argument(
        "rom_file_path", metavar="rom.gb", help="DMG/GBC ROM to disassemble"
    )
    parser.add_argument(
        "output_directory_path",
        metavar="output_dir",
        default="output",
        nargs="?",
        help="where to generate files (defaults to `./output')",
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
