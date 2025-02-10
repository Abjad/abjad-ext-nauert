import abjad
import abjadext.nauert


def test_WeightedSearchTree___call___01():
    definition = {"divisors": (2, 3, 5, 7), "max_depth": 3, "max_divisions": 2}
    search_tree = abjadext.nauert.WeightedSearchTree(definition)
    q_grid = abjadext.nauert.QGrid()
    a = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(0), ["A"], index=1),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    b = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(1, 5), ["B"], index=2),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    c = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(1, 4), ["C"], index=3),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    d = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(1, 3), ["D"], index=4),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    e = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(2, 5), ["E"], index=5),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    f = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(1, 2), ["F"], index=6),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    g = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(3, 5), ["G"], index=7),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    h = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(2, 3), ["H"], index=8),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    i = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(3, 4), ["I"], index=9),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    j = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(4, 5), ["J"], index=10),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    k = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(1), ["K"], index=11),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    q_grid.fit_q_events([a, b, c, d, e, f, g, h, i, j, k])
    q_grids = search_tree(q_grid)
    assert [q_grid.root_node.rtm_format for q_grid in q_grids] == [
        "(1 (1 1))",
        "(1 (2 1))",
        "(1 (1 2))",
        "(1 (4 1))",
        "(1 (3 2))",
        "(1 (2 3))",
        "(1 (1 4))",
        "(1 (6 1))",
        "(1 (5 2))",
        "(1 (4 3))",
        "(1 (3 4))",
        "(1 (2 5))",
        "(1 (1 6))",
    ]
