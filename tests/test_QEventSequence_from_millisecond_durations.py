import itertools

import pytest

import abjad
import abjadext.nauert

test_time_segments = [
    (116, 255),
    (279, 580),
    (627, 720),
    (743, 1300),
    (1324, 1509),
    (1533, 2090),
    (2113, 2833),
    (3320, 3390),
    (3413, 4087),
    (4203, 4389),
    (4412, 4807),
    (4946, 5898),
    (6478, 6687),
    (6711, 6780),
    (6803, 7082),
    (7129, 7314),
    (7361, 7918),
    (7988, 8290),
    (8313, 8452),
    (8475, 8731),
    (8754, 8824),
    (8847, 9009),
    (9033, 9172),
    (9404, 9474),
    (9520, 9961),
    (10356, 10449),
    (10472, 10588),
    (10612, 10960),
    (11006, 11262),
    (11285, 11378),
    (11401, 11517),
    (11540, 12237),
    (12423, 12957),
    (13073, 13166),
    (13189, 13700),
    (13769, 13862),
    (14095, 14234),
    (14350, 15279),
    (15372, 15952),
    (15999, 16091),
    (16138, 16324),
    (16765, 16997),
    (17043, 17136),
    (17160, 17345),
    (17392, 17578),
    (18599, 19342),
]


def test_QEventSequence_from_millisecond_durations_01():
    r"""Test basic functionality."""

    durations = abjad.math.difference_series([x[0] for x in test_time_segments])
    q_events = abjadext.nauert.QEventSequence.from_millisecond_durations(durations)
    offsets = [0] + list(itertools.accumulate(durations))
    sequence = [
        abjadext.nauert.PitchedQEvent(abjad.Offset(offset), (abjad.NamedPitch("c'"),))
        for offset in offsets[:-1]
    ]
    sequence.append(abjadext.nauert.TerminalQEvent(abjad.Offset(offsets[-1])))
    assert q_events == abjadext.nauert.QEventSequence(tuple(sequence))


def test_QEventSequence_from_millisecond_durations_02():
    r"""Silences are not fused."""

    durations = [100, -100, 100, -100, -100, 100]
    q_events = abjadext.nauert.QEventSequence.from_millisecond_durations(
        durations, fuse_silences=False
    )

    assert q_events == abjadext.nauert.QEventSequence(
        (
            abjadext.nauert.PitchedQEvent(abjad.Offset(0), (abjad.NamedPitch("c'"),)),
            abjadext.nauert.SilentQEvent(abjad.Offset(100)),
            abjadext.nauert.PitchedQEvent(abjad.Offset(200), (abjad.NamedPitch("c'"),)),
            abjadext.nauert.SilentQEvent(abjad.Offset(300)),
            abjadext.nauert.SilentQEvent(abjad.Offset(400)),
            abjadext.nauert.PitchedQEvent(abjad.Offset(500), (abjad.NamedPitch("c'"),)),
            abjadext.nauert.TerminalQEvent(abjad.Offset(600)),
        )
    )


def test_QEventSequence_from_millisecond_durations_03():
    r"""Silences are fused."""

    durations = [100, -100, 100, -100, -100, 100]
    q_events = abjadext.nauert.QEventSequence.from_millisecond_durations(
        durations, fuse_silences=True
    )

    assert q_events == abjadext.nauert.QEventSequence(
        (
            abjadext.nauert.PitchedQEvent(abjad.Offset(0), (abjad.NamedPitch("c'"),)),
            abjadext.nauert.SilentQEvent(abjad.Offset(100)),
            abjadext.nauert.PitchedQEvent(abjad.Offset(200), (abjad.NamedPitch("c'"),)),
            abjadext.nauert.SilentQEvent(abjad.Offset(300)),
            abjadext.nauert.PitchedQEvent(abjad.Offset(500), (abjad.NamedPitch("c'"),)),
            abjadext.nauert.TerminalQEvent(abjad.Offset(600)),
        )
    )
