from charybdis import cli

ROM_FILE_PATH = "rom.gbc"


def test_get_parser__rom_file_path() -> None:
    parser = cli.get_parser()
    args = parser.parse_args([ROM_FILE_PATH])
    assert ROM_FILE_PATH == args.rom_file_path


def test_get_parser__output_directory_path() -> None:
    parser = cli.get_parser()
    args = parser.parse_args([ROM_FILE_PATH])
    assert "output" == args.output_directory_path
    args = parser.parse_args([ROM_FILE_PATH, "foo"])
    assert "foo" == args.output_directory_path


def test_get_parser__overwrite() -> None:
    parser = cli.get_parser()
    args = parser.parse_args(["--overwrite", ROM_FILE_PATH])
    assert args.overwrite
    args = parser.parse_args([ROM_FILE_PATH])
    assert not args.overwrite
    args = parser.parse_args(["--no-overwrite", ROM_FILE_PATH])
    assert not args.overwrite
