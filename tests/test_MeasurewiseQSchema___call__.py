import abjad
import abjadext.nauert


def test_MeasurewiseQSchema___call___01():
    schema = abjadext.nauert.MeasurewiseQSchema()
    schema(abjad.Duration(5000))
