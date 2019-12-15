import abjad
import abjadext.nauert


def test_TerminalQEvent___init___01():

    q_event = abjadext.nauert.TerminalQEvent(154)

    assert q_event.offset == abjad.Offset(154)
