from typing import Any, Callable, IO, Optional

import pyparsing as pp

from charybdis.ann import types

ParseAction = Callable[[str, int, pp.ParseResults], Any]

BASE_PREFIXES = {
    2: "0b",
    16: "0x",
}


def tokens(f: Callable[[pp.ParseResults], Any]) -> ParseAction:
    def action(s: str, loc: int, tokens: pp.ParseResults) -> Any:
        return f(tokens)

    return action


def parse_int(base: int) -> ParseAction:
    def action(tokens: pp.ParseResults) -> Optional[list[Any]]:
        assert len(tokens) == 1
        assert isinstance(tokens[0], str)
        prefix = BASE_PREFIXES.get(base, "")
        token = tokens[0]
        if token.startswith(prefix):
            token = token[len(prefix) :]
        return [int(token, base)]

    return tokens(action)


pp.ParserElement.set_default_whitespace_chars("")

addr = pp.Word(pp.hexnums, exact=4).set_parse_action(parse_int(16))("addr")
bank = pp.Word(pp.hexnums, exact=2).set_parse_action(parse_int(16))("bank")
comment = pp.Combine(";" + pp.Opt(pp.CharsNotIn("\n")))
integer = (
    pp.Combine("0b" + pp.Word("01")).set_parse_action(parse_int(2))
    | pp.Combine("0x" + pp.Word(pp.hexnums)).set_parse_action(parse_int(16))
    | pp.Word(pp.nums).set_parse_action(parse_int(10))
)
label = pp.Combine(pp.Char(pp.identchars) + pp.Opt(pp.Word(pp.identbodychars)))("label")
u8 = pp.Literal("u8").set_parse_action(tokens(lambda t: types.PrimitiveType.U8))
u16 = pp.Literal("u16").set_parse_action(tokens(lambda t: types.PrimitiveType.U16))

bank_addr = pp.Group(bank + ":" + addr).set_parse_action(
    tokens(lambda t: types.BankAddr(t[0].bank, t[0].addr))
)("addr")

ann_type = pp.Forward()
array_type = pp.Group("[" + integer("size") + "]" + ann_type("type")).set_parse_action(
    tokens(lambda t: types.ArrayType(type=t[0].type, size=t[0].size))
)
pointer_type = pp.Group("*" + ann_type("ty")).set_parse_action(
    tokens(lambda t: types.PointerType(t[0].ty))
)
primitive_type = u8 | u16
ann_type <<= array_type | pointer_type | primitive_type


opt_type = pp.Group("," + pp.Opt(pp.White()) + ann_type("type")).set_parse_action(
    tokens(lambda t: t[0].type)
)
ann = pp.Group(
    bank_addr + " " + label + pp.Opt(opt_type)("type") + pp.Opt(comment)
).set_parse_action(
    tokens(
        lambda t: types.Ann(t[0].addr, t[0].label, (t[0].type and t[0].type[0]) or None)
    )
)


def parse_ann(line: str) -> types.Ann:
    return ann.parse_string(line, parse_all=True)[0]  # type: ignore


def parse_ann_file(f: IO[str]) -> list[types.Ann]:
    return [parse_ann(line.strip()) for line in f]
