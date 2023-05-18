# charybdis
Type-aware disassembler for Game Boy / Game Boy Color

`charybdis` converts ROM files into a RGBDS-compatible source tree with a Makefile. Building the project produces a ROM which is identical to what `charybdis` was given. If a symbol table is provided, it is used to annotate the source tree.

### Differences from `mgbdis`
This software is inspired by [mattcurie/mgbdis](https://github.com/mattcurie/mgbdis) and should be helpful in similar situations. However, there are some key differences:
* No use of RGBDS symbol format. By using a more expressive alternative, a variety of primitive (and complex) types are supported.
* RAM can be annotated.

## Installation
WIP (see [#4](https://github.com/mn-revival/charybdis/issues/4))

## Usage
Up-to-date information about how to use `charybdis` is displayed when executing it with the `--help` flag. Example:

```
$ charybdis --help
usage: charybdis [-h] [--overwrite | --no-overwrite] rom.gb [output_dir]

positional arguments:
  rom.gb                DMG/GBC ROM to disassemble
  output_dir            where to generate files (defaults to `./output')

options:
  -h, --help            show this help message and exit
  --overwrite, --no-overwrite
                        do/don't overwrite output directory
```

## Development
First, make sure you have Python and [Poetry](https://python-poetry.org/) installed. Then, run:

```
$ poetry install
$ pre-commit install
```

To execute the program:
```
$ poetry run cli
```
