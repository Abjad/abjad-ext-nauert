import decimal

import abjad
import abjadext.nauert
import pytest


def test_PitchedQEvent___init___01():
    q_event = abjadext.nauert.PitchedQEvent(abjad.Offset(130), [0, 1, 4])
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
    a = abjadext.nauert.PitchedQEvent(abjad.Offset(1000), [0])
    b = abjadext.nauert.PitchedQEvent(abjad.Offset(1000), [0])
    assert a == b


def test_PitchedQEvent___eq___02():
    a = abjadext.nauert.PitchedQEvent(abjad.Offset(1000), [0])
    b = abjadext.nauert.PitchedQEvent(abjad.Offset(1000), [0], ["foo", "bar", "baz"])
    c = abjadext.nauert.PitchedQEvent(abjad.Offset(9999), [0])
    d = abjadext.nauert.PitchedQEvent(abjad.Offset(1000), [0, 1, 4])
    assert a != b
    assert a != c
    assert a != d


def test_PitchedQEvent___eq___03():
    a = abjadext.nauert.TerminalQEvent(abjad.Offset(100))
    b = abjadext.nauert.PitchedQEvent(abjad.Offset(100), [0])
    c = abjadext.nauert.SilentQEvent(abjad.Offset(100))
    assert a != b
    assert a != c


def test_SilentQEvent___init___01():
    q_event = abjadext.nauert.SilentQEvent(abjad.Offset(130))
    assert q_event.offset == abjad.Offset(130)
    assert q_event.attachments == ()


def test_SilentQEvent___init___02():
    attachments = ["foo", "bar", "baz"]
    q_event = abjadext.nauert.SilentQEvent(
        abjad.Offset(155, 7), attachments=attachments
    )
    assert q_event.offset == abjad.Offset(155, 7)
    assert q_event.attachments == ("foo", "bar", "baz")


def test_SilentQEvent___eq___01():
    a = abjadext.nauert.SilentQEvent(abjad.Offset(1000))
    b = abjadext.nauert.SilentQEvent(abjad.Offset(1000))
    assert a == b


def test_SilentQEvent___eq___02():
    a = abjadext.nauert.SilentQEvent(abjad.Offset(1000))
    b = abjadext.nauert.SilentQEvent(abjad.Offset(1000), ["foo", "bar", "baz"])
    c = abjadext.nauert.SilentQEvent(abjad.Offset(9999))
    assert a != b
    assert a != c


def test_TerminalQEvent___init___01():
    q_event = abjadext.nauert.TerminalQEvent(abjad.Offset(154))
    assert q_event.offset == abjad.Offset(154)


def test_TerminalQEvent___eq___01():
    a = abjadext.nauert.TerminalQEvent(abjad.Offset(1000))
    b = abjadext.nauert.TerminalQEvent(abjad.Offset(1000))
    assert a == b


def test_TerminalQEvent___eq___02():
    a = abjadext.nauert.TerminalQEvent(abjad.Offset(1000))
    b = abjadext.nauert.TerminalQEvent(abjad.Offset(9000))
    assert a != b


def test_TerminalQEvent___eq___03():
    a = abjadext.nauert.TerminalQEvent(abjad.Offset(100))
    b = abjadext.nauert.PitchedQEvent(abjad.Offset(100), [0])
    c = abjadext.nauert.SilentQEvent(abjad.Offset(100))
    assert a != b
    assert a != c


def test_QEvent_from_offset_pitches_attachments():
    q_event = abjadext.nauert.QEvent.from_offset_pitches_attachments(
        abjad.Offset(100), 1, ("foo",)
    )
    assert isinstance(q_event, abjadext.nauert.PitchedQEvent)
    assert q_event.offset == 100
    assert q_event.pitches == (abjad.NamedPitch(1),)
    assert q_event.attachments == ("foo",)


def test_QEvent_from_offset_pitches_attachments_with_incorrectly_typed_pitches():
    with pytest.raises(TypeError):
        abjadext.nauert.QEvent.from_offset_pitches_attachments(
            100, decimal.Decimal(0), ("foo",)
        )
