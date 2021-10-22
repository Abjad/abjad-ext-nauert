import abjadext.nauert


def test_UnweightedSearchTree___call___01():

    definition = {2: {2: {2: None}, 3: None}, 5: None}
    search_tree = abjadext.nauert.UnweightedSearchTree(definition)
    q_grid = abjadext.nauert.QGrid()
    a = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(0, attachments=["A"], index=1), 0, 1
    )
    b = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((1, 5), attachments=["B"], index=2), 0, 1
    )
    c = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((1, 4), attachments=["C"], index=3), 0, 1
    )
    d = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((1, 3), attachments=["D"], index=4), 0, 1
    )
    e = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((2, 5), attachments=["E"], index=5), 0, 1
    )
    f = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((1, 2), attachments=["F"], index=6), 0, 1
    )
    g = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((3, 5), attachments=["G"], index=7), 0, 1
    )
    h = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((2, 3), attachments=["H"], index=8), 0, 1
    )
    i = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((3, 4), attachments=["I"], index=9), 0, 1
    )
    j = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((4, 5), attachments=["J"], index=10), 0, 1
    )
    k = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(1, attachments=["K"], index=11), 0, 1
    )
    q_grid.fit_q_events([a, b, c, d, e, f, g, h, i, j, k])

    q_grids = search_tree(q_grid)

    assert q_grids[0].root_node.rtm_format == "(1 (1 1))"
    assert q_grids[1].root_node.rtm_format == "(1 (1 1 1 1 1))"
