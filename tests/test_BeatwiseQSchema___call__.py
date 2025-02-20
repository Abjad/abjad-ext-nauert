import abjad

import nauert


def test_BeatwiseQSchema___call___01():
    schema = nauert.BeatwiseQSchema()
    schema(abjad.Duration(5000))
