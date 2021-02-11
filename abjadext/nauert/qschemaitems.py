import abc
import typing

import abjad

from .searchtrees import SearchTree


class QSchemaItem:
    """
    Abstract q-schema item.

    Represents a change of state in the timeline of a quantization process.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_search_tree", "_tempo")

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, search_tree=None, tempo=None):
        if search_tree is not None:
            assert isinstance(search_tree, SearchTree)
        self._search_tree = search_tree
        if tempo is not None:
            if isinstance(tempo, tuple):
                tempo = abjad.MetronomeMark(*tempo)
            assert not tempo.is_imprecise
        self._tempo = tempo

    ### SPECIAL METHODS ###

    def __format__(self, format_specification="") -> str:
        """
        Formats q schema item.

        Set `format_specification` to `''` or `'storage'`. Interprets `''`
        equal to `'storage'`.
        """
        if format_specification in ("", "storage"):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def search_tree(self):
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

    >>> q_schema_item = nauert.BeatwiseQSchemaItem()
    >>> string = abjad.storage(q_schema_item)
    >>> print(string)
    nauert.BeatwiseQSchemaItem()

    ..  container:: example

        Defines a change in tempo:

        >>> q_schema_item = nauert.BeatwiseQSchemaItem(tempo=((1, 4), 60))
        >>> string = abjad.storage(q_schema_item)
        >>> print(string)
        nauert.BeatwiseQSchemaItem(
            tempo=abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 4),
                units_per_minute=60,
                ),
            )

    ..  container:: example

        Defines a change in beatspan:

        >>> q_schema_item = nauert.BeatwiseQSchemaItem(beatspan=(1, 8))
        >>> string = abjad.storage(q_schema_item)
        >>> print(string)
        nauert.BeatwiseQSchemaItem(
            beatspan=abjad.Duration(1, 8),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_beatspan",)

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, beatspan=None, search_tree=None, tempo=None):
        QSchemaItem.__init__(self, search_tree=search_tree, tempo=tempo)
        if beatspan is not None:
            beatspan = abjad.Duration(beatspan)
            assert 0 < beatspan
        self._beatspan = beatspan

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

        >>> q_schema_item = nauert.MeasurewiseQSchemaItem(tempo=((1, 4), 60))
        >>> string = abjad.storage(q_schema_item)
        >>> print(string)
        nauert.MeasurewiseQSchemaItem(
            tempo=abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 4),
                units_per_minute=60,
                ),
            )

    ..  container:: example

        Defines a change in time signature:

        >>> q_schema_item = nauert.MeasurewiseQSchemaItem(time_signature=(6, 8))
        >>> string = abjad.storage(q_schema_item)
        >>> print(string)
        nauert.MeasurewiseQSchemaItem(
            time_signature=abjad.TimeSignature((6, 8)),
            )

    ..  container:: example

        Tests for beatspan given a defined time signature:

        >>> q_schema_item.beatspan
        Duration(1, 8)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_time_signature", "_use_full_measure")

    ### INITIALIZER ###

    def __init__(
        self,
        search_tree=None,
        tempo=None,
        time_signature=None,
        use_full_measure=None,
    ):
        QSchemaItem.__init__(self, search_tree=search_tree, tempo=tempo)
        if time_signature is not None:
            time_signature = abjad.TimeSignature(time_signature)
        self._time_signature = time_signature
        if use_full_measure is not None:
            use_full_measure = bool(use_full_measure)
        self._use_full_measure = use_full_measure

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
