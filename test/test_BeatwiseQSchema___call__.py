import abjad
import abjadext.nauert


def test_BeatwiseQSchema___call___01():

    schema = abjadext.nauert.BeatwiseQSchema()

    target = schema(5000)
