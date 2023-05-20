import string
from typing import Any, IO, Optional

import pyparsing as pp

from charybdis.ann import types


basic_symbol_type = pp.Literal("code") | pp.Literal("data")
symbol_length = pp.Word(pp.hexnums, exact=4).set_parse_action(
    lambda s, l, t: int(t[0], 16)
)


def parse_basic_symbol(s: str, l: int, t: pp.ParseResults) -> Any:
    ty: types.AnnType
    match t[0].type:
        case "code":
            ty = types.CodeType(size=t[0].size)
        case "data":
            ty = types.PrimitiveType.U8
            if t[0].size > 1:
                ty = types.ArrayType(type=types.PrimitiveType.U8, size=t[0].size)
    return ty


basic_symbol = pp.Group(
    "." + basic_symbol_type("type") + ":" + symbol_length("size")
).set_parse_action(parse_basic_symbol)
image_width = pp.Group(":w" + pp.Word(pp.nums)("digits")).set_parse_action(
    lambda s, l, t: int(t[0].digits, 10)
)
image_symbol = pp.Group(
    ".image" + ":" + symbol_length("size") + pp.Opt(image_width)("width")
).set_parse_action(
    lambda s, l, t: types.ImageType(
        size=t[0].size, width=(t[0].width and t[0].width[0]) or None
    )
)


symbol = image_symbol | basic_symbol
symbol_line = pp.Group(
    pp.Word(pp.hexnums, exact=2)("bank")
    + ":"
    + pp.Word(pp.hexnums, exact=4)("addr")
    + " "
    + symbol("symbol")
).set_parse_action(
    lambda s, l, t: types.ann(
        bank=int(t[0].bank, 16), addr=int(t[0].addr, 16), label="", type=t[0].symbol[0]
    )
)
symbol_line_opt = (symbol_line | pp.Opt(pp.White())).set_parse_action(
    lambda s, l, t: t[0] if len(t) == 1 and isinstance(t[0], types.Ann) else []
)

comment = pp.Combine(";" + pp.Opt(pp.Word(string.printable)))
line = pp.Group(symbol_line_opt("opt_sym") + pp.Opt(comment)).set_parse_action(
    lambda s, l, t: t[0].opt_sym if isinstance(t[0].opt_sym, types.Ann) else []
)


def parse_sym_line(raw_line: str) -> Optional[types.Ann]:
    result = line.parse_string(raw_line, parse_all=True)
    return result[0] if len(result) == 1 else None


def parse_sym_file(f: IO[str]) -> list[types.Ann]:
    anns = []
    for line in f:
        ann_opt = parse_sym_line(line.strip())
        if ann_opt is not None:
            anns.append(ann_opt)
    return anns
