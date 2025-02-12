import abjad
import abjadext.nauert


def test_QGridContainer___eq___01():
    a = abjadext.nauert.QGridContainer((1, 1), children=[])
    b = abjadext.nauert.QGridContainer((1, 1), children=[])

    assert format(a) == format(b)
    assert a != b


def test_QGridContainer___eq___02():
    a = abjadext.nauert.QGridContainer(
        (1, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )
    b = abjadext.nauert.QGridContainer(
        (1, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )

    assert format(a) == format(b)
    assert a != b


def test_QGridContainer___eq___03():
    a = abjadext.nauert.QGridContainer((1, 1), children=[])
    b = abjadext.nauert.QGridContainer((2, 1), children=[])
    c = abjadext.nauert.QGridContainer(
        (1, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )
    d = abjadext.nauert.QGridContainer(
        (2, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )
    e = abjadext.nauert.QGridContainer(
        (2, 1),
        children=[abjadext.nauert.QGridLeaf(abjad.Duration(2))],
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
