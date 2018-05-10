import abjad
import abjadext.nauert


def test_QGridLeaf___eq___01():
    a = abjadext.nauert.QGridLeaf(1, [])
    b = abjadext.nauert.QGridLeaf(1, [])
    assert format(a) == format(b)
    assert a != b


def test_QGridLeaf___eq___02():
    a = abjadext.nauert.QGridLeaf(1, [])
    b = abjadext.nauert.QGridLeaf(1, [abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(1000), 0.5)])
    c = abjadext.nauert.QGridLeaf(2, [])
    d = abjadext.nauert.QGridLeaf(2, [abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(1000), 0.5)])
    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
