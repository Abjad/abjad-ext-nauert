import abjad
import abjadext.nauert


def test_QEventSequence_from_tempo_scaled_durations_01():
    r'''Test basic functionality.
    '''

    durations = [abjad.Duration(x) for x in
        [(1, 4), (1, 3), (1, 7), (2, 5), (3, 4)]]
    tempo = abjad.MetronomeMark((1, 4), 55)
    q_events = abjadext.nauert.QEventSequence.from_tempo_scaled_durations(
        durations, tempo)

    assert q_events == abjadext.nauert.QEventSequence((
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(0, 1),
            (abjad.NamedPitch("c'"),)
            ),
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(12000, 11),
            (abjad.NamedPitch("c'"),)
            ),
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(28000, 11),
            (abjad.NamedPitch("c'"),)
            ),
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(244000, 77),
            (abjad.NamedPitch("c'"),)
            ),
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(34400, 7),
            (abjad.NamedPitch("c'"),)
            ),
        abjadext.nauert.TerminalQEvent(
            abjad.Offset(630400, 77)
            )
    ))


def test_QEventSequence_from_tempo_scaled_durations_02():
    r'''Silences are fused.
    '''

    durations = [abjad.Duration(x) for x in
        [(1, 4), (-1, 4), (1, 4), (1, 4), (-1, 4), (-1, 4), (1, 4)]]
    tempo = abjad.MetronomeMark((1, 4), 77)
    q_events = abjadext.nauert.QEventSequence.from_tempo_scaled_durations(
        durations, tempo)

    assert q_events == abjadext.nauert.QEventSequence((
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(0, 1),
            (abjad.NamedPitch("c'"),)
            ),
        abjadext.nauert.SilentQEvent(
            abjad.Offset(60000, 77)
            ),
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(120000, 77),
            (abjad.NamedPitch("c'"),)
            ),
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(180000, 77),
            (abjad.NamedPitch("c'"),)
            ),
        abjadext.nauert.SilentQEvent(
            abjad.Offset(240000, 77)
            ),
        abjadext.nauert.PitchedQEvent(
            abjad.Offset(360000, 77),
            (abjad.NamedPitch("c'"),)
            ),
        abjadext.nauert.TerminalQEvent(
            abjad.Offset(60000, 11)
            )
    ))
