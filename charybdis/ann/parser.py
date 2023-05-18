from typing import Any, Callable, Optional

import pyparsing as pp

from charybdis.ann import types

BASE_PREFIXES = {
    2: "0b",
    16: "0x",
}


def action_parse_int(
    base: int,
) -> Callable[[str, int, pp.ParseResults], Optional[list[Any]]]:
    def action(s: str, loc: int, tokens: pp.ParseResults) -> Optional[list[Any]]:
        assert len(tokens) == 1
        assert isinstance(tokens[0], str)
        prefix = BASE_PREFIXES.get(base, "")
        token = tokens[0]
        if token.startswith(prefix):
            token = token[: len(prefix)]
        return [int(token, base)]

    return action


pp.ParserElement.set_default_whitespace_chars("")

addr = pp.Word(pp.hexnums, exact=4).set_parse_action(action_parse_int(16))("addr")
bank = pp.Word(pp.hexnums, exact=2).set_parse_action(action_parse_int(16))("bank")
comment = pp.Combine(";" + pp.Opt(pp.CharsNotIn("\n")))
decimal = (
    pp.Combine("0b" + pp.Word("01")).set_parse_action(action_parse_int(2))
    | pp.Combine("0x" + pp.Word(pp.hexnums)).set_parse_action(action_parse_int(16))
    | pp.Word(pp.nums).set_parse_action(action_parse_int(10))
)
label = pp.Combine(pp.Char(pp.identchars) + pp.Opt(pp.Word(pp.identbodychars)))("label")
u8 = pp.Literal("u8").add_parse_action(lambda s, l, t: [types.PrimitiveType.U8])
u16 = pp.Literal("u16").add_parse_action(lambda s, l, t: [types.PrimitiveType.U16])

bank_addr = pp.Group(bank + ":" + addr).set_parse_action(
    lambda s, l, t: [types.BankAddr(t[0].bank, t[0].addr)]
)("addr")

array_type = pp.Group(
    "[" + decimal("size") + "]" + pp.Forward("_type")("ty")
).add_parse_action(lambda s, l, t: [types.ArrayType(type=t.ty, size=t.size)])
pointer_type = pp.Group("*" + pp.Forward("_type")("ty")).add_parse_action(
    lambda s, l, t: [types.PointerType(t[0].ty)]
)
primitive_type = u8 | u16
ann_type = (array_type | pointer_type | primitive_type)("type")


opt_type = pp.Group("," + pp.Opt(pp.White()) + ann_type("ty")).add_parse_action(
    lambda s, l, t: [t[0].ty]
)
ann = pp.Group(bank_addr + " " + label).set_parse_action(
    lambda s, l, t: [
        types.Ann(addr=t[0].addr[0], label=t[0].label, type=(t[0].type or None))
    ]
)


def parse_ann(line: str) -> types.Ann:
    return ann.parse_string(line, parse_all=True)[0]  # type: ignore
