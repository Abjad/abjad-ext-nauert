import abjad
from abjadext import nauert


def test_ConcatenatingGraceHandler___call___01():
    grace_handler = nauert.ConcatenatingGraceHandler()
    quantizer = nauert.Quantizer()
    durations = [1000, 1, 999]
    pitches = [0, None, 0]
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        tuple(zip(durations, pitches))
    )
    result = quantizer(q_event_sequence, grace_handler=grace_handler)
    assert abjad.lilypond(result) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                \tempo 4=60
                %%% \time 4/4 %%%
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
    quantizer = nauert.Quantizer()
    durations = [1000, 1, 999]
    pitches = [0, None, 0]
    q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        tuple(zip(durations, pitches))
    )
    result = quantizer(q_event_sequence, grace_handler=grace_handler)
    assert abjad.lilypond(result) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                \tempo 4=60
                %%% \time 4/4 %%%
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
