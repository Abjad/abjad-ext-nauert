import abjad

import nauert


def test_QGridLeaf___eq___01():
    a = nauert.QGridLeaf(abjad.Duration(1), [])
    b = nauert.QGridLeaf(abjad.Duration(1), [])
    assert format(a) == format(b)
    assert a != b


def test_QGridLeaf___eq___02():
    a = nauert.QGridLeaf(abjad.Duration(1), [])
    sqe = nauert.SilentQEvent(abjad.Offset(1000))
    b = nauert.QGridLeaf(
        abjad.Duration(1),
        [nauert.QEventProxy(sqe, abjad.Offset(0.5))],
    )
    c = nauert.QGridLeaf(abjad.Duration(2), [])
    d = nauert.QGridLeaf(
        abjad.Duration(2),
        [nauert.QEventProxy(sqe, abjad.Offset(0.5))],
    )
    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
