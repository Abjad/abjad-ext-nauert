import abjad
import abjadext.nauert


def test_SilentQEvent___eq___01():

    a = abjadext.nauert.SilentQEvent(1000)
    b = abjadext.nauert.SilentQEvent(1000)

    assert a == b


def test_SilentQEvent___eq___02():

    a = abjadext.nauert.SilentQEvent(1000)
    b = abjadext.nauert.SilentQEvent(1000, ['foo', 'bar', 'baz'])
    c = abjadext.nauert.SilentQEvent(9999)

    assert a != b
    assert a != c
