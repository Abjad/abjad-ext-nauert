import pickle

import abjad

import nauert


def test_QGrid_pickle_01():
    q_grid = nauert.QGrid(
        root_node=nauert.QGridContainer(
            (1, 1),
            children=[
                nauert.QGridLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    q_event_proxies=[
                        nauert.QEventProxy(
                            nauert.SilentQEvent(abjad.Offset(100)),
                            abjad.Offset(0.5),
                        )
                    ],
                )
            ],
        ),
        next_downbeat=nauert.QGridLeaf(
            preprolated_duration=abjad.Duration(1, 1),
            q_event_proxies=[
                nauert.QEventProxy(
                    nauert.TerminalQEvent(abjad.Offset(200)), abjad.Offset(0.9)
                )
            ],
        ),
    )
    pickled = pickle.loads(pickle.dumps(q_grid))
    assert repr(pickled) == repr(q_grid)
    assert pickled is not q_grid
    assert pickled != q_grid
