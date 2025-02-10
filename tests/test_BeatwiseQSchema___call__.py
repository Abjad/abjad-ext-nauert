import abjad
import abjadext.nauert


def test_BeatwiseQSchema___call___01():
    schema = abjadext.nauert.BeatwiseQSchema()
    schema(abjad.Duration(5000))
