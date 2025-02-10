import abjad
import abjadext.nauert


def test_QGrid_subdivide_leaf_01():
    q_grid = abjadext.nauert.QGrid()
    a = abjadext.nauert.QEventProxy(
        abjadext.nauert.PitchedQEvent(abjad.Offset(0), [0]), abjad.Offset(0)
    )
    b = abjadext.nauert.QEventProxy(
        abjadext.nauert.PitchedQEvent(abjad.Offset(9, 20), [1]), abjad.Offset(9, 20)
    )
    c = abjadext.nauert.QEventProxy(
        abjadext.nauert.PitchedQEvent(abjad.Offset(1, 2), [2]), abjad.Offset(1, 2)
    )
    d = abjadext.nauert.QEventProxy(
        abjadext.nauert.PitchedQEvent(abjad.Offset(11, 20), [3]), abjad.Offset(11, 20)
    )
    e = abjadext.nauert.QEventProxy(
        abjadext.nauert.PitchedQEvent(abjad.Offset(1), [4]), abjad.Offset(1)
    )
    q_grid.leaves[0].q_event_proxies.extend([a, b, c, d])
    q_grid.leaves[1].q_event_proxies.append(e)
    result = q_grid.subdivide_leaf(q_grid.leaves[0], (2, 3))
    assert result == [a, b, c, d]

    root_node = abjadext.nauert.QGridContainer(
        (1, 1),
        children=[
            abjadext.nauert.QGridLeaf(
                preprolated_duration=abjad.Duration(2, 1), q_event_proxies=[]
            ),
            abjadext.nauert.QGridLeaf(
                preprolated_duration=abjad.Duration(3, 1), q_event_proxies=[]
            ),
        ],
    )
    assert format(q_grid.root_node) == format(root_node)
