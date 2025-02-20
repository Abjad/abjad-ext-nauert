import abjad

import nauert


def test_DiscardingGraceHandler___call___01():
    grace_handler = nauert.DiscardingGraceHandler()
    durations = [1000, 1, 1, 998, 1, 999, 1, 999]
    pitches = [0, 1, 2, 3, 4, 5, 6, None]
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        tuple(zip(durations, pitches))
    )
    result = nauert.quantize(q_event_sequence, grace_handler=grace_handler)
    assert abjad.lilypond(result) == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                %%% \time 4/4 %%%
                \tempo 4=60
                c'4
                ef'4
                f'4
                r4
            }
        }
        """
    ), print(abjad.lilypond(result))
    assert len(grace_handler.discarded_q_events) == 3
    assert grace_handler.discarded_q_events[0] == (
        nauert.PitchedQEvent(abjad.Offset(1000), [1]),
        nauert.PitchedQEvent(abjad.Offset(1001), [2]),
    )
    assert grace_handler.discarded_q_events[1] == (
        nauert.PitchedQEvent(abjad.Offset(2000), [4]),
    )
    assert grace_handler.discarded_q_events[2] == (
        nauert.PitchedQEvent(abjad.Offset(3000), [6]),
    )
