import abjad
import pickle
import abjadext.nauert


def test_QGrid_pickle_01():
    q_grid = abjadext.nauert.QGrid(
        root_node=abjadext.nauert.QGridContainer(
            preprolated_duration=1,
            children=[
                abjadext.nauert.QGridLeaf(
                    preprolated_duration=1,
                    q_event_proxies=[
                        abjadext.nauert.QEventProxy(
                            abjadext.nauert.SilentQEvent(100),
                            0.5,
                            ),
                        ],
                    ),
                ],
            ),
        next_downbeat=abjadext.nauert.QGridLeaf(
            preprolated_duration=1,
            q_event_proxies=[
                abjadext.nauert.QEventProxy(
                    abjadext.nauert.TerminalQEvent(200),
                    0.9,
                    ),
                ],
            ),
        )
    pickled = pickle.loads(pickle.dumps(q_grid))

    assert format(pickled) == format(q_grid)
    assert pickled is not q_grid
    assert pickled != q_grid, abjad.TestManager.diff(pickled, q_grid, 'Diff:')
