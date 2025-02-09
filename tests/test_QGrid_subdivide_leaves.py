import abjad
import abjadext.nauert


def test_QGrid_subdivide_leaves_01():
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
    q_grid.leaves[0].q_event_proxies.extend([a, b, c, d])
    q_grid.leaves[1].q_event_proxies.extend([e, f, g])
    assert q_grid.root_node.rtm_format == "1"

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    assert q_events == [a, b, c, d, e, f]
    assert q_grid.root_node.rtm_format == "(1 (1 1))"

    q_grid.leaves[0].q_event_proxies.extend([a, b])
    q_grid.leaves[1].q_event_proxies.extend([c, d, e])
    q_grid.leaves[2].q_event_proxies.append(f)
    q_events = q_grid.subdivide_leaves([(0, (1, 1)), (1, (1, 1))])
    assert q_events == [a, b, c, d, e, f]
    assert q_grid.root_node.rtm_format == "(1 ((1 (1 1)) (1 (1 1))))"


def test_QGrid_subdivide_leaves_02():
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
    q_grid.leaves[0].q_event_proxies.extend([a, b, c, d])
    q_grid.leaves[1].q_event_proxies.extend([e, f, g])
    assert q_grid.root_node.rtm_format == "1"

    q_events = q_grid.subdivide_leaves([(0, (1, 1))])
    assert q_events == [a, b, c, d, e, f]
    assert q_grid.root_node.rtm_format == "(1 (1 1))"

    q_grid.leaves[0].q_event_proxies.extend([a, b])
    q_grid.leaves[1].q_event_proxies.extend([c, d, e])
    q_grid.leaves[2].q_event_proxies.append(f)
    q_events = q_grid.subdivide_leaves([(0, (3, 4, 5))])
    assert q_events == [a, b, c]
    assert q_grid.root_node.rtm_format == "(1 ((1 (3 4 5)) 1))"
