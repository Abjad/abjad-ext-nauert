import abjad
import abjadext.nauert


def test_MeasurewiseQSchema___init___01():
    item_a = abjadext.nauert.MeasurewiseQSchemaItem(
        search_tree=abjadext.nauert.UnweightedSearchTree({2: None})
    )
    metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 76)
    item_b = abjadext.nauert.MeasurewiseQSchemaItem(tempo=metronome_mark)
    time_signature = abjad.TimeSignature((3, 4))
    item_c = abjadext.nauert.MeasurewiseQSchemaItem(time_signature=time_signature)
    item_d = abjadext.nauert.MeasurewiseQSchemaItem(use_full_measure=True)
    time_signature = abjad.TimeSignature((5, 8))
    schema = abjadext.nauert.MeasurewiseQSchema(
        {2: item_a, 4: item_b, 7: item_c, 8: item_d},
        search_tree=abjadext.nauert.UnweightedSearchTree({3: None}),
        tempo=(abjad.Duration(1, 8), 58),
        time_signature=time_signature,
        use_full_measure=False,
    )
    assert len(schema.items) == 4
    assert schema.search_tree == abjadext.nauert.UnweightedSearchTree({3: None})
    assert schema.tempo == abjad.MetronomeMark(abjad.Duration(1, 8), 58)
    assert schema.time_signature == abjad.TimeSignature((5, 8))
    assert schema.use_full_measure is False


def test_MeasurewiseQSchema___init___02():
    schema = abjadext.nauert.MeasurewiseQSchema()

    assert len(schema.items) == 0
    assert schema.search_tree == abjadext.nauert.UnweightedSearchTree()
    assert schema.tempo == abjad.MetronomeMark(abjad.Duration(1, 4), 60)
    assert schema.time_signature == abjad.TimeSignature((4, 4))
    assert schema.use_full_measure is False
