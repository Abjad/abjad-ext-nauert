import abjad

import nauert


def test_BeatwiseQSchema___init___01():
    item_a = nauert.BeatwiseQSchemaItem(
        search_tree=nauert.UnweightedSearchTree({2: None})
    )
    metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 76)
    item_b = nauert.BeatwiseQSchemaItem(tempo=metronome_mark)
    item_c = nauert.BeatwiseQSchemaItem(beatspan=abjad.Duration(1, 8))

    schema = nauert.BeatwiseQSchema(
        {2: item_a, 4: item_b, 7: item_c},
        beatspan=abjad.Duration(1, 32),
        search_tree=nauert.UnweightedSearchTree({3: None}),
        tempo=abjad.MetronomeMark(abjad.Duration(1, 16), 32),
    )
    assert len(schema.items) == 3
    assert schema.beatspan == abjad.Duration(1, 32)
    assert schema.search_tree == nauert.UnweightedSearchTree({3: None})
    assert schema.tempo == abjad.MetronomeMark(abjad.Duration(1, 16), 32)


def test_BeatwiseQSchema___init___02():
    schema = nauert.BeatwiseQSchema()
    assert len(schema.items) == 0
    assert schema.beatspan == abjad.Duration(1, 4)
    assert schema.search_tree == nauert.UnweightedSearchTree()
    assert schema.tempo == abjad.MetronomeMark(abjad.Duration(1, 4), 60)
