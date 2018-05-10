import abjad
import abjadext.nauert


def test_SilentQEvent___init___01():

    q_event = abjadext.nauert.SilentQEvent(130)

    assert q_event.offset == abjad.Offset(130)
    assert q_event.attachments == ()


def test_SilentQEvent___init___02():

    q_event = abjadext.nauert.SilentQEvent(
        abjad.Offset(155, 7),
        attachments = ['foo', 'bar', 'baz']
        )

    assert q_event.offset == abjad.Offset(155, 7)
    assert q_event.attachments == ('foo', 'bar', 'baz')
