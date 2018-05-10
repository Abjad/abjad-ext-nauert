import abjad
import copy
import abjadext.nauert


def test_QGridContainer___copy___01():

    tree = abjadext.nauert.QGridContainer(
        preprolated_duration=1,
        children=[
            abjadext.nauert.QGridLeaf(preprolated_duration=1),
            abjadext.nauert.QGridContainer(
                preprolated_duration=2,
                children=[
                    abjadext.nauert.QGridLeaf(preprolated_duration=3),
                    abjadext.nauert.QGridContainer(
                        preprolated_duration=4,
                        children=[
                            abjadext.nauert.QGridLeaf(preprolated_duration=1),
                            abjadext.nauert.QGridLeaf(preprolated_duration=1),
                            abjadext.nauert.QGridLeaf(preprolated_duration=1)
                        ])
                ]),
            abjadext.nauert.QGridLeaf(preprolated_duration=2)
        ])

    copied = copy.deepcopy(tree)

    assert format(tree) == format(copied)
    assert tree is not copied
    assert tree[0] is not copied[0]
    assert tree[1] is not copied[1]
    assert tree[2] is not copied[2]
