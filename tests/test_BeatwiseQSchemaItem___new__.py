import pytest

import abjad
import abjadext.nauert


@pytest.mark.parametrize(
    "init_kwargs, beatspan, search_tree, tempo",
    [
        ({}, None, None, None),
        ({"tempo": ((1, 4), 60)}, None, None, abjad.MetronomeMark((1, 4), 60)),
        ({"beatspan": (1, 8)}, abjad.Duration(1, 8), None, None),
        (
            {"beatspan": (1, 8), "tempo": ((1, 4), 57)},
            abjad.Duration(1, 8),
            None,
            abjad.MetronomeMark((1, 4), 57),
        ),
    ],
)
def test_BeatwiseQSchemaItem___new___00(init_kwargs, beatspan, search_tree, tempo):
    item = abjadext.nauert.BeatwiseQSchemaItem(**init_kwargs)
    assert item.beatspan == beatspan
    assert item.search_tree == search_tree
    assert item.tempo == tempo


def test_BeatwiseQSchemaItem___new___01():
    tempo = abjad.MetronomeMark(textual_indication="lento")
    with pytest.raises(AssertionError):
        item = abjadext.nauert.BeatwiseQSchemaItem(tempo=tempo)
