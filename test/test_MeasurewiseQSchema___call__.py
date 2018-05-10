import abjad
import abjadext.nauert


def test_MeasurewiseQSchema___call___01():

    schema = abjadext.nauert.MeasurewiseQSchema()

    target = schema(5000)
