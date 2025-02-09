import abjad
import abjadext.nauert


def test_QuantizationJob___call___01():
    job_id = 1
    definition = {2: {2: {2: None}, 3: None}, 5: None}
    search_tree = abjadext.nauert.UnweightedSearchTree(definition)
    q_event_proxies = [
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(0), ["A"], index=1),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(1, 5), ["B"], index=2),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(1, 4), ["C"], index=3),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(1, 3), ["D"], index=4),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(2, 5), ["E"], index=5),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(1, 2), ["F"], index=6),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(3, 5), ["G"], index=7),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(2, 3), ["H"], index=8),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(3, 4), ["I"], index=9),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(4, 5), ["J"], index=10),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
        abjadext.nauert.QEventProxy(
            abjadext.nauert.SilentQEvent(abjad.Offset(1), ["K"], index=11),
            abjad.Offset(0),
            abjad.Offset(1),
        ),
    ]
    job = abjadext.nauert.QuantizationJob(job_id, search_tree, q_event_proxies)
    job()
    assert len(job.q_grids) == 10

    rtm_formats = [q_grid.root_node.rtm_format for q_grid in job.q_grids]
    rtm_formats.sort(reverse=True)
    assert rtm_formats == [
        "1",
        "(1 (1 1))",
        "(1 (1 1 1 1 1))",
        "(1 ((1 (1 1)) (1 (1 1))))",
        "(1 ((1 (1 1)) (1 (1 1 1))))",
        "(1 ((1 (1 1 1)) (1 (1 1))))",
        "(1 ((1 (1 1 1)) (1 (1 1 1))))",
        "(1 ((1 (1 1 1)) (1 ((1 (1 1)) (1 (1 1))))))",
        "(1 ((1 ((1 (1 1)) (1 (1 1)))) (1 (1 1 1))))",
        "(1 ((1 ((1 (1 1)) (1 (1 1)))) (1 ((1 (1 1)) (1 (1 1))))))",
    ], rtm_formats
