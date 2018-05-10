import abjad
import abjadext.nauert


def test_UnweightedSearchTree__find_divisible_leaf_indices_and_subdivisions_01():

    definition = {
        2: {
            2: {
                2: None
            },
            3: None
        },
        5: None
    }
    search_tree = abjadext.nauert.UnweightedSearchTree(definition)

    q_grid = abjadext.nauert.QGrid()
    a = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(0,      ['A']), 0, 1)
    b = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 5), ['B']), 0, 1)
    c = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 4), ['C']), 0, 1)
    d = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 3), ['D']), 0, 1)
    e = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((2, 5), ['E']), 0, 1)
    f = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 2), ['F']), 0, 1)
    g = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((3, 5), ['G']), 0, 1)
    h = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((2, 3), ['H']), 0, 1)
    i = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((3, 4), ['I']), 0, 1)
    j = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((4, 5), ['J']), 0, 1)
    k = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(1,      ['K']), 0, 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g, h, i, j, k])

    indices, subdivisions = search_tree._find_divisible_leaf_indices_and_subdivisions(q_grid)

    assert indices == [0]
    assert subdivisions == [((1, 1), (1, 1, 1, 1, 1))]
