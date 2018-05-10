import abjad
import abjadext.nauert


def test_MeasurewiseQSchema___getitem___01():

    schema = abjadext.nauert.MeasurewiseQSchema()

    assert schema[0] == schema[1] == schema[2] == {
        'search_tree': abjadext.nauert.UnweightedSearchTree(),
        'tempo': abjad.MetronomeMark((1, 4), 60),
        'time_signature': abjad.TimeSignature((4, 4)),
        'use_full_measure': False,
    }


def test_MeasurewiseQSchema___getitem___02():

    item_a = abjadext.nauert.MeasurewiseQSchemaItem(search_tree=abjadext.nauert.UnweightedSearchTree({2: None}))
    item_b = abjadext.nauert.MeasurewiseQSchemaItem(tempo=((1, 4), 76))
    item_c = abjadext.nauert.MeasurewiseQSchemaItem(time_signature=(3, 4))
    item_d = abjadext.nauert.MeasurewiseQSchemaItem(
        search_tree=abjadext.nauert.UnweightedSearchTree({5: None}),
        use_full_measure=True
        )

    schema = abjadext.nauert.MeasurewiseQSchema(
        {2: item_a, 4: item_b, 7: item_c, 8: item_d},
        search_tree=abjadext.nauert.UnweightedSearchTree({3: None}),
        tempo=((1, 8), 58),
        time_signature=(5, 8),
        use_full_measure=False,
        )

    assert schema[0] == schema[1] == {
        'search_tree': abjadext.nauert.UnweightedSearchTree({3: None}),
        'tempo': abjad.MetronomeMark((1, 8), 58),
        'time_signature': abjad.TimeSignature((5, 8)),
        'use_full_measure': False,
    }

    assert schema[2] == schema[3] == {
        'search_tree': abjadext.nauert.UnweightedSearchTree({2: None}),
        'tempo': abjad.MetronomeMark((1, 8), 58),
        'time_signature': abjad.TimeSignature((5, 8)),
        'use_full_measure': False,
    }

    assert schema[4] == schema[5] == schema[6] == {
        'search_tree': abjadext.nauert.UnweightedSearchTree({2: None}),
        'tempo': abjad.MetronomeMark((1, 4), 76),
        'time_signature': abjad.TimeSignature((5, 8)),
        'use_full_measure': False,
    }

    assert schema[7] == {
        'search_tree': abjadext.nauert.UnweightedSearchTree({2: None}),
        'tempo': abjad.MetronomeMark((1, 4), 76),
        'time_signature': abjad.TimeSignature((3, 4)),
        'use_full_measure': False,
    }

    assert schema[8] == schema[9] == schema[1000] == {
        'search_tree': abjadext.nauert.UnweightedSearchTree({5: None}),
        'tempo': abjad.MetronomeMark((1, 4), 76),
        'time_signature': abjad.TimeSignature((3, 4)),
        'use_full_measure': True,
    }
