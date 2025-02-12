import abjad
import abjadext.nauert


def test_QGrid___eq___01():
    a = abjadext.nauert.QGrid()
    b = abjadext.nauert.QGrid()
    assert format(a) == format(b)
    assert a != b


def test_QGrid___eq___02():
    a = abjadext.nauert.QGrid(
        root_node=abjadext.nauert.QGridContainer(
            (1, 1),
            children=[
                abjadext.nauert.QGridLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    q_event_proxies=[
                        abjadext.nauert.QEventProxy(
                            abjadext.nauert.SilentQEvent(abjad.Offset(100)),
                            abjad.Offset(0.5),
                        )
                    ],
                )
            ],
        ),
        next_downbeat=abjadext.nauert.QGridLeaf(
            preprolated_duration=abjad.Duration(1, 1),
            q_event_proxies=[
                abjadext.nauert.QEventProxy(
                    abjadext.nauert.TerminalQEvent(abjad.Offset(200)), abjad.Offset(0.9)
                )
            ],
        ),
    )
    b = abjadext.nauert.QGrid(
        root_node=abjadext.nauert.QGridContainer(
            (1, 1),
            children=[
                abjadext.nauert.QGridLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    q_event_proxies=[
                        abjadext.nauert.QEventProxy(
                            abjadext.nauert.SilentQEvent(abjad.Offset(100)),
                            abjad.Offset(0.5),
                        )
                    ],
                )
            ],
        ),
        next_downbeat=abjadext.nauert.QGridLeaf(
            preprolated_duration=abjad.Duration(1, 1),
            q_event_proxies=[
                abjadext.nauert.QEventProxy(
                    abjadext.nauert.TerminalQEvent(abjad.Offset(200)), abjad.Offset(0.9)
                )
            ],
        ),
    )
    assert format(a) == format(b)
    assert a != b


def test_QGrid___eq___03():
    a = abjadext.nauert.QGrid()
    b = abjadext.nauert.QGrid(
        root_node=abjadext.nauert.QGridContainer(
            (1, 1),
            children=[
                abjadext.nauert.QGridLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    q_event_proxies=[
                        abjadext.nauert.QEventProxy(
                            abjadext.nauert.SilentQEvent(abjad.Offset(100)),
                            abjad.Offset(0.5),
                        )
                    ],
                )
            ],
        )
    )
    c = abjadext.nauert.QGrid(
        next_downbeat=abjadext.nauert.QGridLeaf(
            preprolated_duration=abjad.Duration(1, 1),
            q_event_proxies=[
                abjadext.nauert.QEventProxy(
                    abjadext.nauert.TerminalQEvent(abjad.Offset(200)), abjad.Offset(0.9)
                )
            ],
        )
    )
    d = (
        abjadext.nauert.QGrid(
            root_node=abjadext.nauert.QGridContainer(
                (1, 1),
                children=[
                    abjadext.nauert.QGridLeaf(
                        preprolated_duration=abjad.Duration(1, 1),
                        q_event_proxies=[
                            abjadext.nauert.QEventProxy(
                                abjadext.nauert.SilentQEvent(abjad.Offset(100)),
                                abjad.Offset(0.5),
                            )
                        ],
                    )
                ],
            ),
            next_downbeat=abjadext.nauert.QGridLeaf(
                preprolated_duration=abjad.Duration(1, 1),
                q_event_proxies=[
                    abjadext.nauert.QEventProxy(
                        abjadext.nauert.TerminalQEvent(abjad.Offset(200)),
                        abjad.Offset(0.9),
                    )
                ],
            ),
        ),
    )
    assert a != b
    assert a != c
    assert a != d
    assert b != c
    assert b != d
    assert c != d
