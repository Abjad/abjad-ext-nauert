import copy

import abjad

import nauert


def test_QGridLeaf___copy___01():
    leaf = nauert.QGridLeaf(abjad.Duration(1))
    copied = copy.deepcopy(leaf)
    assert format(leaf) == format(copied)
    assert leaf != copied
    assert leaf is not copied


def test_QGridLeaf___copy___02():
    sqe = nauert.SilentQEvent(abjad.Offset(1000))
    leaf = nauert.QGridLeaf(
        abjad.Duration(2),
        [nauert.QEventProxy(sqe, abjad.Offset(0.5))],
    )
    copied = copy.deepcopy(leaf)
    assert format(leaf) == format(copied)
    assert leaf != copied
    assert leaf is not copied
