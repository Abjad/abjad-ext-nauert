import abjad
import abjadext.nauert


def test_QGrid_distance_01():

    q_grid = abjadext.nauert.QGrid()

    assert q_grid.distance is None

    a = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(0,        ['A']), 0)
    q_grid.fit_q_events([a])
    assert q_grid.distance == abjad.Offset(0)

    b = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 20),  ['B']), (1, 20))
    q_grid.fit_q_events([b])
    assert q_grid.distance == abjad.Offset(1, 40)

    c = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((9, 20),  ['C']), (9, 20))
    q_grid.fit_q_events([c])
    assert q_grid.distance == abjad.Offset(1, 6)

    d = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 2),   ['D']), (1, 2))
    q_grid.fit_q_events([d])
    assert q_grid.distance == abjad.Offset(1, 4)

    e = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((11, 20), ['E']), (11, 20))
    q_grid.fit_q_events([e])
    assert q_grid.distance == abjad.Offset(29, 100)

    f = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((19, 20), ['F']), (19, 20))
    q_grid.fit_q_events([f])
    assert q_grid.distance == abjad.Offset(1, 4)

    g = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(1,        ['G']), 1)
    q_grid.fit_q_events([g])
    assert q_grid.distance == abjad.Offset(3, 14)

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    q_grid.fit_q_events(q_events)

    assert q_grid.distance == abjad.Offset(1, 35)
