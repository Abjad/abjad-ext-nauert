import abjad

import nauert


def test_QGrid_distance_01():
    q_grid = nauert.QGrid()
    assert q_grid.distance is None

    a = nauert.QEventProxy(nauert.SilentQEvent(abjad.Offset(0), ["A"]), abjad.Offset(0))
    q_grid.fit_q_events([a])
    assert q_grid.distance == abjad.Offset(0)

    b = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 20), ["B"]), abjad.Offset(1, 20)
    )
    q_grid.fit_q_events([b])
    assert q_grid.distance == abjad.Offset(1, 40)

    c = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(9, 20), ["C"]), abjad.Offset(9, 20)
    )
    q_grid.fit_q_events([c])
    assert q_grid.distance == abjad.Offset(1, 6)

    d = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(1, 2), ["D"]), abjad.Offset(1, 2)
    )
    q_grid.fit_q_events([d])
    assert q_grid.distance == abjad.Offset(1, 4)

    e = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(11, 20), ["E"]), abjad.Offset(11, 20)
    )
    q_grid.fit_q_events([e])
    assert q_grid.distance == abjad.Offset(29, 100)

    f = nauert.QEventProxy(
        nauert.SilentQEvent(abjad.Offset(19, 20), ["F"]), abjad.Offset(19, 20)
    )
    q_grid.fit_q_events([f])
    assert q_grid.distance == abjad.Offset(1, 4)

    g = nauert.QEventProxy(nauert.SilentQEvent(abjad.Offset(1), ["G"]), abjad.Offset(1))
    q_grid.fit_q_events([g])
    assert q_grid.distance == abjad.Offset(3, 14)

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    q_grid.fit_q_events(q_events)

    assert q_grid.distance == abjad.Offset(1, 35)
