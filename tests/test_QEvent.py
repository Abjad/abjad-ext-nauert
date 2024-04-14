import decimal

import pytest

import abjad
import abjadext.nauert


def test_PitchedQEvent___init___01():
    q_event = abjadext.nauert.PitchedQEvent(130, [0, 1, 4])
    assert q_event.offset == abjad.Offset(130)
    assert q_event.pitches == (
        abjad.NamedPitch(0),
        abjad.NamedPitch(1),
        abjad.NamedPitch(4),
    )
    assert q_event.attachments == ()


def test_PitchedQEvent___init___02():
    q_event = abjadext.nauert.PitchedQEvent(
        abjad.Offset(133, 5),
        [abjad.NamedPitch("fss")],
        attachments=["foo", "bar", "baz"],
    )
    assert q_event.offset == abjad.Offset(133, 5)
    assert q_event.pitches == (abjad.NamedPitch("fss"),)
    assert q_event.attachments == ("foo", "bar", "baz")


def test_PitchedQEvent___eq___01():
    a = abjadext.nauert.PitchedQEvent(1000, [0])
    b = abjadext.nauert.PitchedQEvent(1000, [0])
    assert a == b


def test_PitchedQEvent___eq___02():
    a = abjadext.nauert.PitchedQEvent(1000, [0])
    b = abjadext.nauert.PitchedQEvent(1000, [0], ["foo", "bar", "baz"])
    c = abjadext.nauert.PitchedQEvent(9999, [0])
    d = abjadext.nauert.PitchedQEvent(1000, [0, 1, 4])
    assert a != b
    assert a != c
    assert a != d


def test_PitchedQEvent___eq___03():
    a = abjadext.nauert.TerminalQEvent(100)
    b = abjadext.nauert.PitchedQEvent(100, [0])
    c = abjadext.nauert.SilentQEvent(100)
    assert a != b
    assert a != c


def test_SilentQEvent___init___01():
    q_event = abjadext.nauert.SilentQEvent(130)

    assert q_event.offset == abjad.Offset(130)
    assert q_event.attachments == ()


def test_SilentQEvent___init___02():
    q_event = abjadext.nauert.SilentQEvent(
        abjad.Offset(155, 7), attachments=["foo", "bar", "baz"]
    )

    assert q_event.offset == abjad.Offset(155, 7)
    assert q_event.attachments == ("foo", "bar", "baz")


def test_SilentQEvent___eq___01():
    a = abjadext.nauert.SilentQEvent(1000)
    b = abjadext.nauert.SilentQEvent(1000)
    assert a == b


def test_SilentQEvent___eq___02():
    a = abjadext.nauert.SilentQEvent(1000)
    b = abjadext.nauert.SilentQEvent(1000, ["foo", "bar", "baz"])
    c = abjadext.nauert.SilentQEvent(9999)
    assert a != b
    assert a != c


def test_TerminalQEvent___init___01():
    q_event = abjadext.nauert.TerminalQEvent(154)

    assert q_event.offset == abjad.Offset(154)


def test_TerminalQEvent___eq___01():
    a = abjadext.nauert.TerminalQEvent(1000)
    b = abjadext.nauert.TerminalQEvent(1000)

    assert a == b


def test_TerminalQEvent___eq___02():
    a = abjadext.nauert.TerminalQEvent(1000)
    b = abjadext.nauert.TerminalQEvent(9000)

    assert a != b


def test_TerminalQEvent___eq___03():
    a = abjadext.nauert.TerminalQEvent(100)
    b = abjadext.nauert.PitchedQEvent(100, [0])
    c = abjadext.nauert.SilentQEvent(100)

    assert a != b
    assert a != c


def test_QEvent_from_offset_pitches_attachments():
    q_event = abjadext.nauert.QEvent.from_offset_pitches_attachments(100, 1, ("foo",))
    assert isinstance(q_event, abjadext.nauert.PitchedQEvent)
    assert q_event.offset == 100
    assert q_event.pitches == (abjad.NamedPitch(1),)
    assert q_event.attachments == ("foo",)


def test_QEvent_from_offset_pitches_attachments_with_incorrectly_typed_pitches():
    with pytest.raises(TypeError):
        abjadext.nauert.QEvent.from_offset_pitches_attachments(
            100, decimal.Decimal(0), ("foo",)
        )
