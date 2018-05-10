import abjad
import abjadext.nauert


def test_QGridContainer___eq___01():

    a = abjadext.nauert.QGridContainer(preprolated_duration=1, children=[])
    b = abjadext.nauert.QGridContainer(preprolated_duration=1, children=[])

    assert format(a) == format(b)
    assert a != b


def test_QGridContainer___eq___02():

    a = abjadext.nauert.QGridContainer(preprolated_duration=1, children=[
        abjadext.nauert.QGridLeaf(preprolated_duration=1)
        ])
    b = abjadext.nauert.QGridContainer(preprolated_duration=1, children=[
        abjadext.nauert.QGridLeaf(preprolated_duration=1)
        ])

    assert format(a) == format(b)
    assert a != b


def test_QGridContainer___eq___03():

    a = abjadext.nauert.QGridContainer(preprolated_duration=1, children=[])
    b = abjadext.nauert.QGridContainer(preprolated_duration=2, children=[])
    c = abjadext.nauert.QGridContainer(preprolated_duration=1, children=[
        abjadext.nauert.QGridLeaf(preprolated_duration=1)
        ])
    d = abjadext.nauert.QGridContainer(preprolated_duration=2, children=[
        abjadext.nauert.QGridLeaf(preprolated_duration=1)
        ])
    e = abjadext.nauert.QGridContainer(preprolated_duration=2, children=[
        abjadext.nauert.QGridLeaf(2)
        ])

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
