import abjad

import nauert


def test_MeasurewiseQSchema___call___01():
    schema = nauert.MeasurewiseQSchema()
    schema(abjad.Duration(5000))
