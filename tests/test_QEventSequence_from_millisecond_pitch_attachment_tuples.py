import abjad

import nauert


def test_QEventSequence_from_millisecond_pitch_attachment_tuples_01():
    durations = [100, 200, 100, 300, 350, 400, 600]
    pitches = [0, None, None, [1, 4], None, 5, 7]
    attachments = [("foo",), (), (), (6,), (), ("foobar",), ("foo", "bar")]
    tuples = tuple(zip(durations, pitches, attachments))
    q_events = nauert.QEventSequence.from_millisecond_pitch_attachment_tuples(tuples)
    assert q_events == nauert.QEventSequence(
        (
            nauert.PitchedQEvent(abjad.Offset(0), (abjad.NamedPitch("c'"),), ("foo",)),
            nauert.SilentQEvent(abjad.Offset(100, 1)),
            nauert.PitchedQEvent(
                abjad.Offset(400, 1),
                (abjad.NamedPitch("cs'"), abjad.NamedPitch("e'")),
                (6,),
            ),
            nauert.SilentQEvent(abjad.Offset(700, 1)),
            nauert.PitchedQEvent(
                abjad.Offset(1050, 1), (abjad.NamedPitch("f'"),), ("foobar",)
            ),
            nauert.PitchedQEvent(
                abjad.Offset(1450, 1), (abjad.NamedPitch("g'"),), ("foo", "bar")
            ),
            nauert.TerminalQEvent(abjad.Offset(2050, 1)),
        )
    ), repr(q_events)
