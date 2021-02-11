import pytest

import abjad
from abjadext import nauert


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    print(abjad, abjad.__version__)
    doctest_namespace["abjad"] = abjad
    doctest_namespace["nauert"] = nauert
    # doctest_namespace["f"] = abjad.f
    # doctest_namespace["Infinity"] = abjad.mathtools.Infinity()
    # doctest_namespace["NegativeInfinity"] = abjad.mathtools.NegativeInfinity()
