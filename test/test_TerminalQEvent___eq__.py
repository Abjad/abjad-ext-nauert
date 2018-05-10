import abjad
import abjadext.nauert


def test_TerminalQEvent___eq___01():

    a = abjadext.nauert.TerminalQEvent(1000)
    b = abjadext.nauert.TerminalQEvent(1000)

    assert a == b


def test_TerminalQEvent___eq___02():

    a = abjadext.nauert.TerminalQEvent(1000)
    b = abjadext.nauert.TerminalQEvent(9000)

    assert a != b


def test_TerminalQEvent___eq___03():

    a = abjadext.nauert.TerminalQEvent(100)
    b = abjadext.nauert.PitchedQEvent(100, [0])
    c = abjadext.nauert.SilentQEvent(100)

    assert a != b
    assert a != c
