import abjad

import nauert


def test_CollapsingGraceHandler___call___01():
    grace_handler = nauert.CollapsingGraceHandler()
    durations = [1000, 1, 1, 997]
    pitches = [0, 7, 4, 0]
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
                <c' e' g'>4
                r4
                r4
            }
        }
        """
    ), print(abjad.lilypond(result))


def test_CollapsingGraceHandler___call___02():
    grace_handler = nauert.CollapsingGraceHandler()
    durations = [1000, 1, 1, 1, 997]
    pitches = [0, 7, None, 4, 0]
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
                <c' e' g'>4
                r4
                r4
            }
        }
        """
    ), print(abjad.lilypond(result))


def test_CollapsingGraceHandler___call___03():
    grace_handler = nauert.CollapsingGraceHandler()
    durations = [1000, 1, 1, 1, 997]
    pitches = [0, None, 7, 4, 0]
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
                <c' e' g'>4
                r4
                r4
            }
        }
        """
    ), print(abjad.lilypond(result))


def test_CollapsingGraceHandler___call___04():
    grace_handler = nauert.CollapsingGraceHandler()
    durations = [1000, 1, 1, 1, 997]
    pitches = [0, 4, 7, None, 0]
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
                <c' e' g'>4
                r4
                r4
            }
        }
        """
    ), print(abjad.lilypond(result))
