import copy

import abjad

import nauert


def test_QGridContainer___copy___01():
    tree = nauert.QGridContainer(
        (1, 1),
        children=[
            nauert.QGridLeaf(abjad.Duration(1, 1)),
            nauert.QGridContainer(
                (2, 1),
                children=[
                    nauert.QGridLeaf(abjad.Duration(3, 1)),
                    nauert.QGridContainer(
                        (4, 1),
                        children=[
                            nauert.QGridLeaf(abjad.Duration(1, 1)),
                            nauert.QGridLeaf(abjad.Duration(1, 1)),
                            nauert.QGridLeaf(abjad.Duration(1, 1)),
                        ],
                    ),
                ],
            ),
            nauert.QGridLeaf(abjad.Duration(2, 1)),
        ],
    )
    copied = copy.deepcopy(tree)
    assert format(tree) == format(copied)
    assert tree is not copied
    assert tree[0] is not copied[0]
    assert tree[1] is not copied[1]
    assert tree[2] is not copied[2]
