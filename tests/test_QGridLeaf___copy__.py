import copy

import abjad
import abjadext.nauert


def test_QGridLeaf___copy___01():
    leaf = abjadext.nauert.QGridLeaf(abjad.Duration(1))
    copied = copy.deepcopy(leaf)
    assert format(leaf) == format(copied)
    assert leaf != copied
    assert leaf is not copied


def test_QGridLeaf___copy___02():
    leaf = abjadext.nauert.QGridLeaf(
        abjad.Duration(2),
        [abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(1000), 0.5)],
    )
    copied = copy.deepcopy(leaf)
    assert format(leaf) == format(copied)
    assert leaf != copied
    assert leaf is not copied
