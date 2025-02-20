import abjad
import pytest

import nauert


def test_MeasurewiseQSchemaItem___new___01():
    item = nauert.MeasurewiseQSchemaItem()
    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo is None
    assert item.time_signature is None


def test_MeasurewiseQSchemaItem___new___02():
    metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
    item = nauert.MeasurewiseQSchemaItem(tempo=metronome_mark)
    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo == metronome_mark
    assert item.time_signature is None


def test_MeasurewiseQSchemaItem___new___03():
    time_signature = abjad.TimeSignature((6, 8))
    item = nauert.MeasurewiseQSchemaItem(time_signature=time_signature)
    assert item.beatspan == abjad.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo is None
    assert item.time_signature == time_signature


def test_MeasurewiseQSchemaItem___new___04():
    metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 57)
    time_signature = abjad.TimeSignature((6, 8))
    item = nauert.MeasurewiseQSchemaItem(
        tempo=metronome_mark, time_signature=time_signature
    )
    assert item.beatspan == abjad.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo == metronome_mark
    assert item.time_signature == time_signature


def test_MeasurewiseQSchemaItem___new___05():
    tempo = abjad.MetronomeMark(textual_indication="lento")
    with pytest.raises(AssertionError):
        nauert.MeasurewiseQSchemaItem(tempo=tempo)
