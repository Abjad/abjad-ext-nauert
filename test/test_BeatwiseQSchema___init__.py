import abjad
import abjadext.nauert


def test_BeatwiseQSchema___init___01():

    item_a = abjadext.nauert.BeatwiseQSchemaItem(
        search_tree=abjadext.nauert.UnweightedSearchTree({2: None}))
    item_b = abjadext.nauert.BeatwiseQSchemaItem(tempo=((1, 4), 76))
    item_c = abjadext.nauert.BeatwiseQSchemaItem(beatspan=(1, 8))

    schema = abjadext.nauert.BeatwiseQSchema(
        {2: item_a, 4: item_b, 7: item_c},
        beatspan=abjad.Duration(1, 32),
        search_tree=abjadext.nauert.UnweightedSearchTree({3: None}),
        tempo=abjad.MetronomeMark((1, 16), 32)
        )

    assert len(schema.items) == 3
    assert schema.beatspan == abjad.Duration(1, 32)
    assert schema.search_tree == abjadext.nauert.UnweightedSearchTree({3: None})
    assert schema.tempo == abjad.MetronomeMark((1, 16), 32)


def test_BeatwiseQSchema___init___02():

    schema = abjadext.nauert.BeatwiseQSchema()

    assert len(schema.items) == 0
    assert schema.beatspan == abjad.Duration(1, 4)
    assert schema.search_tree == abjadext.nauert.UnweightedSearchTree()
    assert schema.tempo == abjad.MetronomeMark((1, 4), 60)
