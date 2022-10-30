import abc
import typing

import abjad

from .searchtrees import SearchTree


class QSchemaItem(abc.ABC):
    """
    Abstract q-schema item.

    Represents a change of state in the timeline of a quantization process.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_search_tree", "_tempo")

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        search_tree: SearchTree | None = None,
        tempo: abjad.MetronomeMark | tuple | None = None,
    ):
        if search_tree is not None:
            assert isinstance(search_tree, SearchTree)
        self._search_tree = search_tree
        if tempo is not None:
            if isinstance(tempo, tuple):
                assert len(tempo) == 2
                reference_duration_, units_per_minute = tempo
                reference_duration = abjad.Duration(reference_duration_)
                tempo = abjad.MetronomeMark(
                    reference_duration=reference_duration,
                    units_per_minute=units_per_minute,
                )
            assert not tempo.is_imprecise
        self._tempo = tempo

    ### PUBLIC PROPERTIES ###

    @property
    def search_tree(self) -> typing.Optional[SearchTree]:
        """
        The optionally defined search tree.

        Returns search tree or none.
        """
        return self._search_tree

    @property
    def tempo(self) -> typing.Optional[abjad.MetronomeMark]:
        """
        The optionally defined tempo.
        """
        return self._tempo


class BeatwiseQSchemaItem(QSchemaItem):
    """
    Beatwise q-schema item.

    Represents a change of state in the timeline of an unmetered quantization
    process.

    >>> nauert.BeatwiseQSchemaItem()
    BeatwiseQSchemaItem(beatspan=None, search_tree=None, tempo=None)

    ..  container:: example

        Defines a change in tempo:

        >>> nauert.BeatwiseQSchemaItem(tempo=((1, 4), 60))
        BeatwiseQSchemaItem(beatspan=None, search_tree=None, tempo=MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=60, textual_indication=None, custom_markup=None, decimal=False, hide=False))

    ..  container:: example

        Defines a change in beatspan:

        >>> nauert.BeatwiseQSchemaItem(beatspan=(1, 8))
        BeatwiseQSchemaItem(beatspan=Duration(1, 8), search_tree=None, tempo=None)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_beatspan",)

    ### INITIALIZER ###

    def __init__(
        self,
        beatspan: abjad.typings.Duration | int | None = None,
        search_tree: SearchTree | None = None,
        tempo: abjad.MetronomeMark | tuple | None = None,
    ):
        QSchemaItem.__init__(self, search_tree=search_tree, tempo=tempo)
        if beatspan is not None:
            beatspan = abjad.Duration(beatspan)
            assert 0 < beatspan
        self._beatspan = beatspan

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}(beatspan={self.beatspan!r}, search_tree={self.search_tree!r}, tempo={self.tempo!r})"

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self) -> typing.Optional[abjad.Duration]:
        """
        The optionally defined beatspan duration.
        """
        return self._beatspan


class MeasurewiseQSchemaItem(QSchemaItem):
    """
    Measurewise q-schema item.

    Represents a change of state in the timeline of a metered quantization process.

    >>> q_schema_item = nauert.MeasurewiseQSchemaItem()

    ..  container:: example

        Defines a change in tempo:

        >>> nauert.MeasurewiseQSchemaItem(tempo=((1, 4), 60))
        MeasurewiseQSchemaItem(search_tree=None, tempo=MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=60, textual_indication=None, custom_markup=None, decimal=False, hide=False), time_signature=None, use_full_measure=None)

    ..  container:: example

        Defines a change in time signature:

        >>> nauert.MeasurewiseQSchemaItem(time_signature=(6, 8))
        MeasurewiseQSchemaItem(search_tree=None, tempo=None, time_signature=TimeSignature(pair=(6, 8), hide=False, partial=None), use_full_measure=None)

    ..  container:: example

        Tests for beatspan given a defined time signature:

        >>> nauert.MeasurewiseQSchemaItem(time_signature=(6, 8)).beatspan
        Duration(1, 8)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_time_signature", "_use_full_measure")

    ### INITIALIZER ###

    def __init__(
        self,
        search_tree: SearchTree | None = None,
        tempo: abjad.MetronomeMark | tuple | None = None,
        time_signature: tuple[int, int] | None = None,
        use_full_measure: bool | None = None,
    ):
        QSchemaItem.__init__(self, search_tree=search_tree, tempo=tempo)
        self._time_signature: abjad.TimeSignature | None
        if time_signature is not None:
            self._time_signature = abjad.TimeSignature(time_signature)
        else:
            self._time_signature = None
        if use_full_measure is not None:
            use_full_measure = bool(use_full_measure)
        self._use_full_measure = use_full_measure

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}(search_tree={self.search_tree!r}, tempo={self.tempo!r}, time_signature={self.time_signature!r}, use_full_measure={self.use_full_measure!r})"

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self) -> typing.Optional[abjad.Duration]:
        """
        The beatspan duration, if a time signature was defined.
        """
        if self.time_signature is not None:
            if self.use_full_measure:
                return self.time_signature.duration
            else:
                return abjad.Duration(1, self.time_signature.denominator)
        return None

    @property
    def time_signature(self) -> typing.Optional[abjad.TimeSignature]:
        """
        The optionally defined TimeSignature.
        """
        return self._time_signature

    @property
    def use_full_measure(self) -> typing.Optional[bool]:
        """
        If true, use the full measure as the beatspan.
        """
        return self._use_full_measure
