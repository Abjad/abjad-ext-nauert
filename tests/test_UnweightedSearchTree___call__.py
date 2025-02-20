import abjad

import nauert


def test_UnweightedSearchTree___call___01():
    definition = {2: {2: {2: None}, 3: None}, 5: None}
    search_tree = nauert.UnweightedSearchTree(definition)
    q_grid = nauert.QGrid()
    a = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(0), ["A"], index=1),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    b = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 5), ["B"], index=2),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    c = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 4), ["C"], index=3),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    d = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 3), ["D"], index=4),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    e = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(2, 5), ["E"], index=5),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    f = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 2), ["F"], index=6),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    g = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(3, 5), ["G"], index=7),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    h = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(2, 3), ["H"], index=8),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    i = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(3, 4), ["I"], index=9),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    j = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(4, 5), ["J"], index=10),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    k = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1), ["K"], index=11),
        abjad.Offset(0),
        abjad.Offset(1),
    )
    q_grid.fit_q_events([a, b, c, d, e, f, g, h, i, j, k])
    q_grids = search_tree(q_grid)
    assert q_grids[0].root_node.rtm_format == "(1 (1 1))"
    assert q_grids[1].root_node.rtm_format == "(1 (1 1 1 1 1))"
