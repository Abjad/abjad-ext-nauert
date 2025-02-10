import abjad
import abjadext.nauert


def test_QGrid_fit_q_events_01():
    q_grid = abjadext.nauert.QGrid()
    a = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(0), ["A"]), abjad.Offset(0)
    )
    b = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(1, 20), ["B"]), abjad.Offset(1, 20)
    )
    c = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(9, 20), ["C"]), abjad.Offset(9, 20)
    )
    d = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(1, 2), ["D"]), abjad.Offset(1, 2)
    )
    e = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(11, 20), ["E"]), abjad.Offset(11, 20)
    )
    f = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(19, 20), ["F"]), abjad.Offset(19, 20)
    )
    g = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent(abjad.Offset(1), ["G"]), abjad.Offset(1)
    )
    q_grid.fit_q_events([a, b, c, d, e, f, g])
    assert q_grid.leaves[0].q_event_proxies == [a, b, c, d]
    assert q_grid.leaves[1].q_event_proxies == [e, f, g]

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    q_grid.fit_q_events(q_events)
    assert q_grid.leaves[0].q_event_proxies == [a, b]
    assert q_grid.leaves[1].q_event_proxies == [c, d, e]
    assert q_grid.leaves[2].q_event_proxies == [g, f]
