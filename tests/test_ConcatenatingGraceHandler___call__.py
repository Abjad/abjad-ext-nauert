import abjad

import nauert


def test_ConcatenatingGraceHandler___call___01():
    grace_handler = nauert.ConcatenatingGraceHandler()
    durations = [1000, 1, 999]
    pitches = [0, None, 0]
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
                c'4
                r4
                r4
            }
        }
        """
    ), print(abjad.lilypond(result))


def test_ConcatenatingGraceHandler___call___02():
    grace_handler = nauert.ConcatenatingGraceHandler(discard_grace_rest=False)
    durations = [1000, 1, 999]
    pitches = [0, None, 0]
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
                \grace {
                    r16
                }
                c'4
                r4
                r4
            }
        }
        """
    ), print(abjad.lilypond(result))


def test_ConcatenatingGraceHandler___call___03():
    grace_handler = nauert.ConcatenatingGraceHandler(
        replace_rest_with_final_grace_note=False
    )
    durations = [1000, 1, 999, 1000]
    pitches = [0, 0, None, 0]
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
                \grace {
                    c'16
                }
                r4
                c'4
                r4
            }
        }
        """
    ), print(abjad.lilypond(result))


def test_ConcatenatingGraceHandler___call___04():
    grace_handler = nauert.ConcatenatingGraceHandler(
        replace_rest_with_final_grace_note=True
    )
    durations = [1000, 1, 999, 1000]
    pitches = [0, 0, None, 0]
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
                c'4
                c'4
                r4
            }
        }
        """
    ), print(abjad.lilypond(result))
