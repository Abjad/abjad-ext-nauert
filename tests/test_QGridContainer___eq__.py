import abjad

import nauert


def test_QGridContainer___eq___01():
    a = nauert.QGridContainer((1, 1), children=[])
    b = nauert.QGridContainer((1, 1), children=[])
    assert format(a) == format(b)
    assert a != b


def test_QGridContainer___eq___02():
    a = nauert.QGridContainer(
        (1, 1),
        children=[nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )
    b = nauert.QGridContainer(
        (1, 1),
        children=[nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )
    assert format(a) == format(b)
    assert a != b


def test_QGridContainer___eq___03():
    a = nauert.QGridContainer((1, 1), children=[])
    b = nauert.QGridContainer((2, 1), children=[])
    c = nauert.QGridContainer(
        (1, 1),
        children=[nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )
    d = nauert.QGridContainer(
        (2, 1),
        children=[nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )
    e = nauert.QGridContainer(
        (2, 1),
        children=[nauert.QGridLeaf(abjad.Duration(2))],
    )
    assert a != b
    assert a != c
    assert a != d
    assert a != e
    assert b != c
    assert b != d
    assert b != e
    assert c != d
    assert c != e
    assert d != e
