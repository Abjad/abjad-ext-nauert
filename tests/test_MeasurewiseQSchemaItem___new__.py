import abjad
import abjadext.nauert
import pytest


def test_MeasurewiseQSchemaItem___new___01():
    item = abjadext.nauert.MeasurewiseQSchemaItem()
    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo is None
    assert item.time_signature is None


def test_MeasurewiseQSchemaItem___new___02():
    metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
    item = abjadext.nauert.MeasurewiseQSchemaItem(tempo=metronome_mark)
    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo == metronome_mark
    assert item.time_signature is None


def test_MeasurewiseQSchemaItem___new___03():
    item = abjadext.nauert.MeasurewiseQSchemaItem(time_signature=(6, 8))
    assert item.beatspan == abjad.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo is None
    assert item.time_signature == abjad.TimeSignature((6, 8))


def test_MeasurewiseQSchemaItem___new___04():
    metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 57)
    item = abjadext.nauert.MeasurewiseQSchemaItem(
        tempo=metronome_mark, time_signature=(6, 8)
    )
    assert item.beatspan == abjad.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo == metronome_mark
    assert item.time_signature == abjad.TimeSignature((6, 8))


def test_MeasurewiseQSchemaItem___new___05():
    tempo = abjad.MetronomeMark(textual_indication="lento")
    with pytest.raises(AssertionError):
        abjadext.nauert.MeasurewiseQSchemaItem(tempo=tempo)
