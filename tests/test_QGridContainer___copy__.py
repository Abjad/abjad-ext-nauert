import copy

import abjadext.nauert


def test_QGridContainer___copy___01():
    tree = abjadext.nauert.QGridContainer(
        preprolated_pair=(1, 1),
        children=[
            abjadext.nauert.QGridLeaf(preprolated_duration=(1, 1)),
            abjadext.nauert.QGridContainer(
                preprolated_pair=(2, 1),
                children=[
                    abjadext.nauert.QGridLeaf(preprolated_duration=(3, 1)),
                    abjadext.nauert.QGridContainer(
                        preprolated_pair=(4, 1),
                        children=[
                            abjadext.nauert.QGridLeaf(preprolated_duration=(1, 1)),
                            abjadext.nauert.QGridLeaf(preprolated_duration=(1, 1)),
                            abjadext.nauert.QGridLeaf(preprolated_duration=(1, 1)),
                        ],
                    ),
                ],
            ),
            abjadext.nauert.QGridLeaf(preprolated_duration=(2, 1)),
        ],
    )
    copied = copy.deepcopy(tree)

    assert format(tree) == format(copied)
    assert tree is not copied
    assert tree[0] is not copied[0]
    assert tree[1] is not copied[1]
    assert tree[2] is not copied[2]
