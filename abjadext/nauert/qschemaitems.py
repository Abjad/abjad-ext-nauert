import abc
import typing

import abjad

from . import searchtrees as _searchtrees


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
        search_tree: _searchtrees.SearchTree | None = None,
        tempo: abjad.MetronomeMark | None = None,
    ) -> None:
        if search_tree is not None:
            assert isinstance(search_tree, _searchtrees.SearchTree)
        self._search_tree = search_tree
        if tempo is not None:
            assert isinstance(tempo, abjad.MetronomeMark), repr(tempo)
            assert not tempo.is_imprecise
        self._tempo = tempo

    ### PUBLIC PROPERTIES ###

    @property
    def search_tree(self) -> typing.Optional[_searchtrees.SearchTree]:
        """
        The optionally defined search tree.
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

    ..  container:: example

        Represents a change of state in the timeline of an unmetered
        quantization process:

        >>> nauert.BeatwiseQSchemaItem()
        BeatwiseQSchemaItem(beatspan=None, search_tree=None, tempo=None)

    ..  container:: example

        Defines a change in tempo:

        >>> metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> nauert.BeatwiseQSchemaItem(tempo=metronome_mark)
        BeatwiseQSchemaItem(...)

    ..  container:: example

        Defines a change in beatspan:

        >>> nauert.BeatwiseQSchemaItem(beatspan=abjad.Duration(1, 8))
        BeatwiseQSchemaItem(beatspan=Duration(1, 8), search_tree=None, tempo=None)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_beatspan",)

    ### INITIALIZER ###

    def __init__(
        self,
        beatspan: abjad.Duration | None = None,
        search_tree: _searchtrees.SearchTree | None = None,
        tempo: abjad.MetronomeMark | None = None,
    ) -> None:
        if beatspan is not None:
            assert isinstance(beatspan, abjad.Duration), repr(beatspan)
        QSchemaItem.__init__(self, search_tree=search_tree, tempo=tempo)
        if beatspan is not None:
            beatspan = abjad.Duration(beatspan)
            assert 0 < beatspan
        self._beatspan = beatspan

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        string = f"{type(self).__name__}(beatspan={self.beatspan!r},"
        string += f" search_tree={self.search_tree!r}, tempo={self.tempo!r})"
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self) -> typing.Optional[abjad.Duration]:
        """
        The optionally defined beatspan duration.
        """
        return self._beatspan


class MeasurewiseQSchemaItem(QSchemaItem):
    r"""
    Measurewise q-schema item.

    Represents a change of state in the timeline of a metered quantization process.

    >>> q_schema_item = nauert.MeasurewiseQSchemaItem()

    ..  container:: example

        Defines a change in tempo:

        >>> metronome_mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> mark = nauert.MeasurewiseQSchemaItem(tempo=metronome_mark).tempo
        >>> abjad.lilypond(mark)
        '\\tempo 4=60'

    ..  container:: example

        Defines a change in time signature:

        >>> time_signature = abjad.TimeSignature((6, 8))
        >>> nauert.MeasurewiseQSchemaItem(time_signature=time_signature).time_signature
        TimeSignature(pair=(6, 8), hide=False, partial=None)

    ..  container:: example

        Tests for beatspan given a defined time signature:

        >>> time_signature = abjad.TimeSignature((6, 8))
        >>> nauert.MeasurewiseQSchemaItem(time_signature=time_signature).beatspan
        Duration(1, 8)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_time_signature", "_use_full_measure")

    ### INITIALIZER ###

    def __init__(
        self,
        search_tree: _searchtrees.SearchTree | None = None,
        tempo: abjad.MetronomeMark | None = None,
        time_signature: abjad.TimeSignature | None = None,
        use_full_measure: bool | None = None,
    ):
        if time_signature is not None:
            assert isinstance(time_signature, abjad.TimeSignature), repr(time_signature)
        QSchemaItem.__init__(self, search_tree=search_tree, tempo=tempo)
        self._time_signature: abjad.TimeSignature | None
        if isinstance(time_signature, abjad.TimeSignature):
            self._time_signature = abjad.TimeSignature(time_signature.pair)
        elif isinstance(time_signature, tuple):
            self._time_signature = abjad.TimeSignature(time_signature)
        else:
            assert time_signature is None
            self._time_signature = None
        if use_full_measure is not None:
            use_full_measure = bool(use_full_measure)
        self._use_full_measure = use_full_measure

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        string = f"{type(self).__name__}(search_tree={self.search_tree!r},"
        string += f" tempo={self.tempo!r}, time_signature={self.time_signature!r},"
        string += f" use_full_measure={self.use_full_measure!r})"
        return string

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
        The optionally defined time signature.
        """
        return self._time_signature

    @property
    def use_full_measure(self) -> typing.Optional[bool]:
        """
        If true, use the full measure as the beatspan.
        """
        return self._use_full_measure
