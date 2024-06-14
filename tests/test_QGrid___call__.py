import abjad
import abjadext.nauert


def test_QGrid___call___01():
    q_grid = abjadext.nauert.QGrid()
    a = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(0, ["A"]), 0)
    b = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((1, 20), ["B"]), (1, 20)
    )
    c = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((9, 20), ["C"]), (9, 20)
    )
    d = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 2), ["D"]), (1, 2))
    e = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((11, 20), ["E"]), (11, 20)
    )
    f = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((19, 20), ["F"]), (19, 20)
    )
    g = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(1, ["G"]), 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g])
    result = q_grid((1, 4))

    assert len(result) == 1
    assert repr(result[0]) == """Note("c'4")"""

    annotation = abjad.get.indicator(result[0], dict)
    q_events = annotation["q_events"]

    assert isinstance(q_events, tuple) and len(q_events) == 4
    assert q_events[0].attachments == ("A",)
    assert q_events[1].attachments == ("B",)
    assert q_events[2].attachments == ("C",)
    assert q_events[3].attachments == ("D",)


def test_QGrid___call___02():
    q_grid = abjadext.nauert.QGrid()
    q_grid.subdivide_leaves([(0, (1, 1, 1))])
    q_grid.subdivide_leaves([(1, (1, 1))])
    q_grid.subdivide_leaves([(-2, (1, 1, 1))])
    a = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(0, ["A"]), 0)
    b = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((1, 20), ["B"]), (1, 20)
    )
    c = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((9, 20), ["C"]), (9, 20)
    )
    d = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 2), ["D"]), (1, 2))
    e = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((11, 20), ["E"]), (11, 20)
    )
    f = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((19, 20), ["F"]), (19, 20)
    )
    g = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(1, ["G"]), 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g])
    result = q_grid((1, 4))

    assert isinstance(result, list) and len(result) == 1
    assert abjad.lilypond(result[0]) == abjad.string.normalize(
        r"""
        \tuplet 3/2
        {
            c'8
            c'16
            c'16
            \tuplet 3/2
            {
                c'16
                c'16
                c'16
            }
        }
        """
    ), print(format(result[0]))

    leaves = abjad.select.leaves(result[0])
    leaf = leaves[0]
    annotation = abjad.get.indicator(leaf, dict)
    q_events = annotation["q_events"]
    assert isinstance(q_events, tuple) and len(q_events) == 2
    assert q_events[0].attachments == ("A",)
    assert q_events[1].attachments == ("B",)

    leaf = leaves[1]
    assert not abjad.get.indicator(leaf, dict)

    leaf = leaves[2]
    annotation = abjad.get.indicator(leaf, dict)
    q_events = annotation["q_events"]

    assert isinstance(q_events, tuple) and len(q_events) == 3
    assert q_events[0].attachments == ("C",)
    assert q_events[1].attachments == ("D",)
    assert q_events[2].attachments == ("E",)

    for leaf in leaves[3:6]:
        assert not abjad.get.indicator(leaf, dict)


def test_QGrid___call___03():
    """
    Non-binary works too.
    """

    q_grid = abjadext.nauert.QGrid()
    q_grid.subdivide_leaves([(0, (1, 1))])

    a = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(0, ["A"]), 0)
    b = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((1, 20), ["B"]), (1, 20)
    )
    c = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((9, 20), ["C"]), (9, 20)
    )
    d = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 2), ["D"]), (1, 2))
    e = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((11, 20), ["E"]), (11, 20)
    )
    f = abjadext.nauert.QEventProxy(
        abjadext.nauert.SilentQEvent((19, 20), ["F"]), (19, 20)
    )
    g = abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(1, ["G"]), 1)

    q_grid.fit_q_events([a, b, c, d, e, f, g])

    result = q_grid((1, 3))

    assert isinstance(result, list) and len(result) == 1
    assert abjad.lilypond(result[0]) == abjad.string.normalize(
        r"""
        \tweak edge-height #'(0.7 . 0)
        \tuplet 3/2
        {
            c'4
            c'4
        }
        """
    ), print(format(result[0]))
