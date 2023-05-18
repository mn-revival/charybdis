from charybdis.ann import parser, types


def test_parse_ann():
    ann = types.Ann(
        addr=types.BankAddr(bank=0x01, addr=0x1234), label="Test", type=None
    )
    assert ann == parser.parse_ann("01:1234 Test")
