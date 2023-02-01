import copy

import abjad
import abjadext.nauert


def test_QGridContainer___copy___01():
    tree = abjadext.nauert.QGridContainer(
        preprolated_duration=abjad.Duration(1, 1),
        children=[
            abjadext.nauert.QGridLeaf(preprolated_duration=abjad.Duration(1, 1)),
            abjadext.nauert.QGridContainer(
                preprolated_duration=abjad.Duration(2, 1),
                children=[
                    abjadext.nauert.QGridLeaf(
                        preprolated_duration=abjad.Duration(3, 1)
                    ),
                    abjadext.nauert.QGridContainer(
                        preprolated_duration=abjad.Duration(4, 1),
                        children=[
                            abjadext.nauert.QGridLeaf(
                                preprolated_duration=abjad.Duration(1, 1)
                            ),
                            abjadext.nauert.QGridLeaf(
                                preprolated_duration=abjad.Duration(1, 1)
                            ),
                            abjadext.nauert.QGridLeaf(
                                preprolated_duration=abjad.Duration(1, 1)
                            ),
                        ],
                    ),
                ],
            ),
            abjadext.nauert.QGridLeaf(preprolated_duration=abjad.Duration(2, 1)),
        ],
    )

    copied = copy.deepcopy(tree)

    assert format(tree) == format(copied)
    assert tree is not copied
    assert tree[0] is not copied[0]
    assert tree[1] is not copied[1]
    assert tree[2] is not copied[2]
