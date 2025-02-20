import abjad

import nauert


def test_BeatwiseQSchema___getitem___01():
    schema = nauert.BeatwiseQSchema()
    assert (
        schema[0]
        == schema[1]
        == schema[2]
        == {
            "beatspan": abjad.Duration(1, 4),
            "search_tree": nauert.UnweightedSearchTree(),
            "tempo": abjad.MetronomeMark(abjad.Duration(1, 4), 60),
        }
    )


def test_BeatwiseQSchema___getitem___02():
    item_a = nauert.BeatwiseQSchemaItem(
        search_tree=nauert.UnweightedSearchTree({2: None})
    )
    metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 76)
    item_b = nauert.BeatwiseQSchemaItem(tempo=metronome_mark)
    item_c = nauert.BeatwiseQSchemaItem(
        beatspan=abjad.Duration(1, 8),
        search_tree=nauert.UnweightedSearchTree({5: None}),
    )
    schema = nauert.BeatwiseQSchema(
        {2: item_a, 4: item_b, 7: item_c},
        beatspan=abjad.Duration(1, 32),
        search_tree=nauert.UnweightedSearchTree({3: None}),
        tempo=abjad.MetronomeMark(abjad.Duration(1, 16), 36),
    )
    assert (
        schema[0]
        == schema[1]
        == {
            "beatspan": abjad.Duration(1, 32),
            "search_tree": nauert.UnweightedSearchTree({3: None}),
            "tempo": abjad.MetronomeMark(abjad.Duration(1, 16), 36),
        }
    )
    assert (
        schema[2]
        == schema[3]
        == {
            "beatspan": abjad.Duration(1, 32),
            "search_tree": nauert.UnweightedSearchTree({2: None}),
            "tempo": abjad.MetronomeMark(abjad.Duration(1, 16), 36),
        }
    )
    assert (
        schema[4]
        == schema[5]
        == schema[6]
        == {
            "beatspan": abjad.Duration(1, 32),
            "search_tree": nauert.UnweightedSearchTree({2: None}),
            "tempo": abjad.MetronomeMark(abjad.Duration(1, 4), 76),
        }
    )
    assert (
        schema[7]
        == schema[8]
        == schema[1000]
        == {
            "beatspan": abjad.Duration(1, 8),
            "search_tree": nauert.UnweightedSearchTree({5: None}),
            "tempo": abjad.MetronomeMark(abjad.Duration(1, 4), 76),
        }
    )
