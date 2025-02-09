import abjad
import pytest
from abjadext import nauert


@pytest.fixture(autouse=True)
def inject_abjad_into_doctest_namespace(doctest_namespace):
    """
    Inject Abjad and Nauert into doctest namespace.
    """
    doctest_namespace["abjad"] = abjad
    doctest_namespace["nauert"] = nauert
