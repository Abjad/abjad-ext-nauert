import abjad
import abjadext.nauert


def test_QuantizationJob___init___01():

    job_id = 1
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
    q_event_proxies = [
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(0,      ['A'], index=1), 0, 1),
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 5), ['B'], index=2), 0, 1),
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 4), ['C'], index=3), 0, 1),
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 3), ['D'], index=4), 0, 1),
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((2, 5), ['E'], index=5), 0, 1),
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((1, 2), ['F'], index=6), 0, 1),
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((3, 5), ['G'], index=7), 0, 1),
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((2, 3), ['H'], index=8), 0, 1),
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((3, 4), ['I'], index=9), 0, 1),
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent((4, 5), ['J'], index=10), 0, 1),
        abjadext.nauert.QEventProxy(abjadext.nauert.SilentQEvent(1,      ['K'], index=11), 0, 1)
    ]

    job = abjadext.nauert.QuantizationJob(job_id, search_tree, q_event_proxies)

    assert job.job_id == job_id
    assert job.search_tree == search_tree
    assert job.q_event_proxies == tuple(q_event_proxies)
