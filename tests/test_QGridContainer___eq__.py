import abjad
import abjadext.nauert


def test_QGridContainer___eq___01():
<<<<<<< HEAD
    a = abjadext.nauert.QGridContainer(preprolated_duration=(1, 1), children=[])
    b = abjadext.nauert.QGridContainer(preprolated_duration=(1, 1), children=[])
=======

    a = abjadext.nauert.QGridContainer(
        preprolated_duration=abjad.Duration(1, 1), children=[]
    )
    b = abjadext.nauert.QGridContainer(
        preprolated_duration=abjad.Duration(1, 1), children=[]
    )
>>>>>>> a3d7af7 (CHANGED:)

    assert format(a) == format(b)
    assert a != b


def test_QGridContainer___eq___02():
    a = abjadext.nauert.QGridContainer(
<<<<<<< HEAD
        preprolated_duration=(1, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=(1, 1))],
    )
    b = abjadext.nauert.QGridContainer(
        preprolated_duration=(1, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=(1, 1))],
=======
        preprolated_duration=abjad.Duration(1, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )
    b = abjadext.nauert.QGridContainer(
        preprolated_duration=abjad.Duration(1, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
>>>>>>> a3d7af7 (CHANGED:)
    )

    assert format(a) == format(b)
    assert a != b


def test_QGridContainer___eq___03():
<<<<<<< HEAD
    a = abjadext.nauert.QGridContainer(preprolated_duration=(1, 1), children=[])
    b = abjadext.nauert.QGridContainer(preprolated_duration=(2, 1), children=[])
    c = abjadext.nauert.QGridContainer(
        preprolated_duration=(1, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=(1, 1))],
    )
    d = abjadext.nauert.QGridContainer(
        preprolated_duration=(2, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=(1, 1))],
    )
    e = abjadext.nauert.QGridContainer(
        preprolated_duration=(2, 1), children=[abjadext.nauert.QGridLeaf(2)]
=======

    a = abjadext.nauert.QGridContainer(
        preprolated_duration=abjad.Duration(1, 1), children=[]
    )
    b = abjadext.nauert.QGridContainer(
        preprolated_duration=abjad.Duration(2, 1), children=[]
    )
    c = abjadext.nauert.QGridContainer(
        preprolated_duration=abjad.Duration(1, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )
    d = abjadext.nauert.QGridContainer(
        preprolated_duration=abjad.Duration(2, 1),
        children=[abjadext.nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1))],
    )
    e = abjadext.nauert.QGridContainer(
        preprolated_duration=abjad.Duration(2, 1),
        children=[abjadext.nauert.QGridLeaf(abjad.Duration(2))],
>>>>>>> a3d7af7 (CHANGED:)
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
