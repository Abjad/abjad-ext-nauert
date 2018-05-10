import abjad
import abjadext.nauert


def test_QEventSequence_from_millisecond_pitch_pairs_01():

    durations = [100, 200, 100, 300, 350, 400, 600]
    pitches = [0, None, None, [1, 4], None, 5, 7]
    pairs = tuple(zip(durations, pitches))

    q_events = abjadext.nauert.QEventSequence.from_millisecond_pitch_pairs(
        pairs)

    assert q_events == abjadext.nauert.QEventSequence((
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(0),
            (abjad.NamedPitch("c'"),)
            ),
        abjadext.nauert.SilentQEvent(
            abjad.Offset(100, 1)
            ),
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(400, 1),
            (
                abjad.NamedPitch("cs'"),
                abjad.NamedPitch("e'")
            )
            ),
        abjadext.nauert.SilentQEvent(
            abjad.Offset(700, 1)
            ),
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(1050, 1),
            (abjad.NamedPitch("f'"),)
            ),
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(1450, 1),
            (abjad.NamedPitch("g'"),)
            ),
        abjadext.nauert.TerminalQEvent(
            abjad.Offset(2050, 1),
            )
    ))
