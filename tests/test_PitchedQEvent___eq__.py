import abjadext.nauert


def test_PitchedQEvent___eq___01():
    a = abjadext.nauert.PitchedQEvent(1000, pitches=[0])
    b = abjadext.nauert.PitchedQEvent(1000, pitches=[0])
    assert a == b


def test_PitchedQEvent___eq___02():
    a = abjadext.nauert.PitchedQEvent(1000, pitches=[0])
    b = abjadext.nauert.PitchedQEvent(1000, pitches=[0], index=["foo", "bar", "baz"])
    c = abjadext.nauert.PitchedQEvent(9999, pitches=[0])
    d = abjadext.nauert.PitchedQEvent(1000, pitches=[0, 1, 4])
    assert a != b
    assert a != c
    assert a != d


def test_PitchedQEvent___eq___03():
    a = abjadext.nauert.TerminalQEvent(100)
    b = abjadext.nauert.PitchedQEvent(100, pitches=[0])
    c = abjadext.nauert.SilentQEvent(100)
    assert a != b
    assert a != c
