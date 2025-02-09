import abjad
import abjadext.nauert
import pytest


def test_BeatwiseQSchemaItem___new___01():
    item = abjadext.nauert.BeatwiseQSchemaItem()
    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo is None


def test_BeatwiseQSchemaItem___new___02():
    metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
    item = abjadext.nauert.BeatwiseQSchemaItem(tempo=metronome_mark)
    assert item.beatspan is None
    assert item.search_tree is None
    assert item.tempo == metronome_mark


def test_BeatwiseQSchemaItem___new___03():
    item = abjadext.nauert.BeatwiseQSchemaItem(beatspan=(1, 8))
    assert item.beatspan == abjad.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo is None


def test_BeatwiseQSchemaItem___new___04():
    metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 57)
    item = abjadext.nauert.BeatwiseQSchemaItem(beatspan=(1, 8), tempo=metronome_mark)
    assert item.beatspan == abjad.Duration(1, 8)
    assert item.search_tree is None
    assert item.tempo == metronome_mark


def test_BeatwiseQSchemaItem___new___05():
    tempo = abjad.MetronomeMark(textual_indication="lento")
    with pytest.raises(AssertionError):
        abjadext.nauert.BeatwiseQSchemaItem(tempo=tempo)
