import abjad

import nauert


def test_QEventSequence_from_tempo_scaled_leaves_01():
    staff = abjad.Staff([])
    staff.append(abjad.Note(0, (1, 4)))
    staff.append(abjad.Rest((1, 4)))
    staff.append(abjad.Rest((1, 8)))
    staff.append(abjad.Note(1, (1, 8)))
    staff.append(abjad.Note(1, (1, 8)))
    staff.append(abjad.Note(2, (1, 8)))
    staff.append(abjad.Note(2, (1, 8)))
    staff.append(abjad.Note(3, (1, 8)))
    staff.append(abjad.Skip((1, 4)))
    staff.append(abjad.Rest((1, 4)))
    staff.append(abjad.Note(3, (1, 8)))
    staff.append(abjad.Chord([0, 1, 4], (1, 4)))
    abjad.tie(staff[3:5])
    abjad.tie(staff[5:7])
    tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 55)
    leaves = abjad.select.leaves(staff)
    q_events = nauert.QEventSequence.from_tempo_scaled_leaves(leaves, tempo)
    assert q_events == nauert.QEventSequence(
        (
            nauert.PitchedQEvent(abjad.Offset(0, 1), (abjad.NamedPitch("c'"),)),
            nauert.SilentQEvent(abjad.Offset(12000, 11)),
            nauert.PitchedQEvent(abjad.Offset(30000, 11), (abjad.NamedPitch("cs'"),)),
            nauert.PitchedQEvent(abjad.Offset(42000, 11), (abjad.NamedPitch("d'"),)),
            nauert.PitchedQEvent(abjad.Offset(54000, 11), (abjad.NamedPitch("ef'"),)),
            nauert.SilentQEvent(abjad.Offset(60000, 11)),
            nauert.PitchedQEvent(abjad.Offset(84000, 11), (abjad.NamedPitch("ef'"),)),
            nauert.PitchedQEvent(
                abjad.Offset(90000, 11),
                (
                    abjad.NamedPitch("c'"),
                    abjad.NamedPitch("cs'"),
                    abjad.NamedPitch("e'"),
                ),
            ),
            nauert.TerminalQEvent(abjad.Offset(102000, 11)),
        )
    )


def test_QEventSequence_from_tempo_scaled_leaves_02():
    staff = abjad.Staff([])
    staff.append(abjad.Note(0, (1, 4)))
    staff.append(abjad.Rest((1, 4)))
    staff.append(abjad.Rest((1, 8)))
    staff.append(abjad.Note(1, (1, 8)))
    staff.append(abjad.Note(1, (1, 8)))
    staff.append(abjad.Note(2, (1, 8)))
    staff.append(abjad.Note(2, (1, 8)))
    staff.append(abjad.Note(3, (1, 8)))
    staff.append(abjad.Skip((1, 4)))
    staff.append(abjad.Rest((1, 4)))
    staff.append(abjad.Note(3, (1, 8)))
    staff.append(abjad.Chord([0, 1, 4], (1, 4)))
    abjad.tie(staff[3:5])
    abjad.tie(staff[5:7])
    tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 58)
    abjad.attach(tempo, staff[0], context="Staff")
    tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 77)
    abjad.attach(tempo, staff[9], context="Staff")
    leaves = abjad.select.leaves(staff)
    q_events = nauert.QEventSequence.from_tempo_scaled_leaves(leaves)
    assert q_events == nauert.QEventSequence(
        (
            nauert.PitchedQEvent(abjad.Offset(0, 1), (abjad.NamedPitch("c'"),)),
            nauert.SilentQEvent(abjad.Offset(30000, 29)),
            nauert.PitchedQEvent(abjad.Offset(75000, 29), (abjad.NamedPitch("cs'"),)),
            nauert.PitchedQEvent(abjad.Offset(105000, 29), (abjad.NamedPitch("d'"),)),
            nauert.PitchedQEvent(abjad.Offset(135000, 29), (abjad.NamedPitch("ef'"),)),
            nauert.SilentQEvent(abjad.Offset(150000, 29)),
            nauert.PitchedQEvent(
                abjad.Offset(15600000, 2233), (abjad.NamedPitch("ef'"),)
            ),
            nauert.PitchedQEvent(
                abjad.Offset(16470000, 2233),
                (
                    abjad.NamedPitch("c'"),
                    abjad.NamedPitch("cs'"),
                    abjad.NamedPitch("e'"),
                ),
            ),
            nauert.TerminalQEvent(abjad.Offset(18210000, 2233)),
        )
    )
