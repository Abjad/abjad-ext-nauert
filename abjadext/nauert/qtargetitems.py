import abc
import typing

import abjad

from .qeventproxy import QEventProxy
from .qevents import QEvent
from .qgrid import QGrid
from .quantizationjob import QuantizationJob
from .searchtrees import SearchTree, UnweightedSearchTree


class QTargetItem(abc.ABC):
    """
    Abstract class for QTargetBeat and QTargetMeasure.
    """

    @abc.abstractproperty
    def offset_in_ms(self) -> abjad.Offset:
        raise NotImplementedError

    @abc.abstractproperty
    def duration_in_ms(self) -> abjad.Duration:
        raise NotImplementedError


class QTargetBeat(QTargetItem):
    """
    Q-target beat.

    Represents a single beat in a quantization target.

    ..  container:: example

        >>> beatspan = abjad.Duration(1, 8)
        >>> offset_in_ms = abjad.Offset(1500)
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 56)

        >>> q_target_beat = nauert.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ... )

        >>> q_target_beat
        QTargetBeat(beatspan=Duration(1, 8), offset_in_ms=Offset((1500, 1)), search_tree=UnweightedSearchTree(definition={3: None}), tempo=MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=56, textual_indication=None, custom_markup=None, decimal=False, hide=False))

    Not composer-safe.

    Used internally by the ``quantize`` function.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_beatspan",
        "_grouping",
        "_offset_in_ms",
        "_q_events",
        "_q_grid",
        "_q_grids",
        "_search_tree",
        "_tempo",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        beatspan: abjad.Duration = abjad.Duration(0),
        offset_in_ms: abjad.Offset = abjad.Offset(0),
        search_tree: SearchTree | None = None,
        tempo: abjad.MetronomeMark = abjad.MetronomeMark(abjad.Duration(1, 4), 60),
    ):
        assert isinstance(beatspan, abjad.Duration), repr(beatspan)
        assert isinstance(offset_in_ms, abjad.Offset), repr(offset_in_ms)
        if search_tree is None:
            search_tree = UnweightedSearchTree()
        assert isinstance(search_tree, SearchTree)
        assert isinstance(tempo, abjad.MetronomeMark), repr(tempo)
        assert not tempo.is_imprecise
        q_events: list[QEvent] = []
        q_grids: tuple[QGrid, ...] = ()
        self._beatspan = beatspan
        self._offset_in_ms = offset_in_ms
        self._q_events = q_events
        self._q_grid: QGrid | None = None
        self._q_grids = q_grids
        self._search_tree = search_tree
        self._tempo = tempo

    ### SPECIAL METHODS ###

    def __call__(self, job_id: int) -> typing.Optional[QuantizationJob]:
        """
        Calls q-target beat.
        """
        if not self.q_events:
            return None
        assert all(isinstance(x, QEvent) for x in self.q_events)
        q_event_proxies = []
        for q_event in self.q_events:
            q_event_proxy = QEventProxy(
                q_event,
                self.offset_in_ms,
                self.offset_in_ms + self.duration_in_ms,
            )
            q_event_proxies.append(q_event_proxy)
        return QuantizationJob(job_id, self.search_tree, q_event_proxies)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        string = f"{type(self).__name__}(beatspan={self.beatspan!r},"
        string += f" offset_in_ms={self.offset_in_ms!r},"
        string += f" search_tree={self.search_tree!r}, tempo={self.tempo!r})"
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self) -> abjad.Duration:
        """
        Beatspan of q-target beat.

        >>> beatspan = abjad.Duration(1, 8)
        >>> offset_in_ms = abjad.Offset(1500)
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 56)

        >>> q_target_beat = nauert.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ... )

        >>> q_target_beat.beatspan
        Duration(1, 8)

        """
        return self._beatspan

    @property
    def duration_in_ms(self) -> abjad.Duration:
        """
        Duration in milliseconds of the q-target beat.

        >>> beatspan = abjad.Duration(1, 8)
        >>> offset_in_ms = abjad.Offset(1500)
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 56)

        >>> q_target_beat = nauert.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ... )

        >>> q_target_beat.duration_in_ms
        Duration(3750, 7)

        """
        return self.tempo.duration_to_milliseconds(self.beatspan)

    @property
    def offset_in_ms(self) -> abjad.Offset:
        """
        Offset in milliseconds of q-target beat.

        >>> beatspan = abjad.Duration(1, 8)
        >>> offset_in_ms = abjad.Offset(1500)
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 56)

        >>> q_target_beat = nauert.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ... )

        >>> q_target_beat.offset_in_ms
        Offset((1500, 1))

        """
        return self._offset_in_ms

    @property
    def q_events(self) -> list[QEvent]:
        """
        A list for storing ``QEventProxy`` instances.

        Used internally by the ``quantize`` function.
        """
        return self._q_events

    @property
    def q_grid(self) -> typing.Optional[QGrid]:
        """
        The ``QGrid`` instance selected by a ``Heuristic``.

        Used internally by the ``quantize`` function.
        """
        return self._q_grid

    @property
    def q_grids(self) -> tuple[QGrid, ...]:
        """
        A tuple of ``QGrids`` generated by a ``QuantizationJob``.

        Used internally by the ``quantize`` function.
        """
        return self._q_grids

    @property
    def search_tree(self) -> SearchTree | UnweightedSearchTree:
        """
        Search tree of q-target beat.

        >>> beatspan = abjad.Duration(1, 8)
        >>> offset_in_ms = abjad.Offset(1500)
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 56)

        >>> q_target_beat = nauert.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ... )

        >>> q_target_beat.search_tree
        UnweightedSearchTree(definition={3: None})

        """
        return self._search_tree

    @property
    def tempo(self) -> abjad.MetronomeMark:
        """
        Gets tempo of q-target beat.

        >>> beatspan = abjad.Duration(1, 8)
        >>> offset_in_ms = abjad.Offset(1500)
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 56)

        >>> q_target_beat = nauert.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ... )

        >>> q_target_beat.tempo
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=56, textual_indication=None, custom_markup=None, decimal=False, hide=False)

        """
        return self._tempo


class QTargetMeasure(QTargetItem):
    """
    Q-target measure.

    Represents a single measure in a measurewise quantization target.

    ..  container:: example

        >>> search_tree = nauert.UnweightedSearchTree({2: None})
        >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> time_signature = abjad.TimeSignature((4, 4))

        >>> q_target_measure = nauert.QTargetMeasure(
        ...     offset_in_ms=abjad.Offset(1000),
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     time_signature=time_signature,
        ... )

        >>> q_target_measure
        QTargetMeasure(offset_in_ms=Offset((1000, 1)), search_tree=UnweightedSearchTree(definition={2: None}), tempo=MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=60, textual_indication=None, custom_markup=None, decimal=False, hide=False), use_full_measure=False)

    ..  container:: example

        ``QTargetMeasures`` group ``QTargetBeats``:

        >>> for q_target_beat in q_target_measure.beats:
        ...     print(q_target_beat.offset_in_ms, q_target_beat.duration_in_ms)
        1000 1000
        2000 1000
        3000 1000
        4000 1000

    ..  container:: example

        If ``use_full_measure`` is set, the ``QTargetMeasure`` will only ever
        contain a single ``QTargetBeat`` instance:

        >>> another_q_target_measure = nauert.QTargetMeasure(
        ...     offset_in_ms=abjad.Offset(1000),
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     time_signature=time_signature,
        ...     use_full_measure=True,
        ... )

        >>> for q_target_beat in another_q_target_measure.beats:
        ...     print(q_target_beat.offset_in_ms, q_target_beat.duration_in_ms)
        1000 4000

    Not composer-safe.

    Used internally by the ``quantize`` function.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_beats",
        "_offset_in_ms",
        "_search_tree",
        "_tempo",
        "_time_signature",
        "_use_full_measure",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        offset_in_ms: abjad.Offset = abjad.Offset(0),
        search_tree: SearchTree | None = None,
        time_signature: abjad.TimeSignature = abjad.TimeSignature((4, 4)),
        tempo: abjad.MetronomeMark = abjad.MetronomeMark(abjad.Duration(4, 4)),
        use_full_measure: bool = False,
    ):
        assert isinstance(offset_in_ms, abjad.Offset), repr(offset_in_ms)
        if search_tree is None:
            search_tree = UnweightedSearchTree()
        assert isinstance(search_tree, SearchTree)
        assert isinstance(time_signature, abjad.TimeSignature), repr(time_signature)
        assert isinstance(tempo, abjad.MetronomeMark), repr(tempo)
        assert not tempo.is_imprecise
        _time_signature = abjad.TimeSignature(time_signature.pair)
        use_full_measure = bool(use_full_measure)
        beats = []
        if use_full_measure:
            beatspan = _time_signature.duration
            beat = QTargetBeat(
                beatspan=beatspan,
                offset_in_ms=offset_in_ms,
                search_tree=search_tree,
                tempo=tempo,
            )
            beats.append(beat)
        else:
            beatspan = abjad.Duration(1, _time_signature.denominator)
            current_offset_in_ms = offset_in_ms
            beatspan_duration_in_ms = tempo.duration_to_milliseconds(beatspan)
            for i in range(_time_signature.numerator):
                beat = QTargetBeat(
                    beatspan=beatspan,
                    offset_in_ms=current_offset_in_ms,
                    search_tree=search_tree,
                    tempo=tempo,
                )
                beats.append(beat)
                current_offset_in_ms += beatspan_duration_in_ms
        self._beats = tuple(beats)
        self._offset_in_ms = offset_in_ms
        self._search_tree = search_tree
        self._tempo = tempo
        self._time_signature = _time_signature
        self._use_full_measure = use_full_measure

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        string = f"{type(self).__name__}(offset_in_ms={self.offset_in_ms!r},"
        string += f" search_tree={self.search_tree!r}, tempo={self.tempo!r},"
        string += f" use_full_measure={self.use_full_measure!r})"
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self) -> tuple:
        """
        Gets the tuple of ``QTargetBeats`` contained by the ``QTargetMeasure``.

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=abjad.Offset(1000),
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ... )

            >>> for q_target_beat in q_target_measure.beats:
            ...     q_target_beat
            ...
            QTargetBeat(beatspan=Duration(1, 4), offset_in_ms=Offset((1000, 1)), search_tree=UnweightedSearchTree(definition={2: None}), tempo=MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=60, textual_indication=None, custom_markup=None, decimal=False, hide=False))
            QTargetBeat(beatspan=Duration(1, 4), offset_in_ms=Offset((2000, 1)), search_tree=UnweightedSearchTree(definition={2: None}), tempo=MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=60, textual_indication=None, custom_markup=None, decimal=False, hide=False))
            QTargetBeat(beatspan=Duration(1, 4), offset_in_ms=Offset((3000, 1)), search_tree=UnweightedSearchTree(definition={2: None}), tempo=MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=60, textual_indication=None, custom_markup=None, decimal=False, hide=False))
            QTargetBeat(beatspan=Duration(1, 4), offset_in_ms=Offset((4000, 1)), search_tree=UnweightedSearchTree(definition={2: None}), tempo=MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=60, textual_indication=None, custom_markup=None, decimal=False, hide=False))

        """
        return self._beats

    @property
    def duration_in_ms(self) -> abjad.Duration:
        """
        Gets duration in milliseconds of the ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=abjad.Offset(1000),
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ... )

            >>> q_target_measure.duration_in_ms
            Duration(4000, 1)

        """
        return self.tempo.duration_to_milliseconds(self.time_signature.duration)

    @property
    def offset_in_ms(self) -> abjad.Offset:
        """
        Gets offset in milliseconds of the ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=abjad.Offset(1000),
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ... )

            >>> q_target_measure.offset_in_ms
            Offset((1000, 1))

        """
        return self._offset_in_ms

    @property
    def search_tree(self) -> SearchTree:
        """
        Gets the search tree of ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=abjad.Offset(1000),
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ... )

            >>> q_target_measure.search_tree
            UnweightedSearchTree(definition={2: None})

        """
        return self._search_tree

    @property
    def tempo(self) -> abjad.MetronomeMark:
        """
        Gets the tempo of ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=abjad.Offset(1000),
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ... )

            >>> q_target_measure.tempo
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=60, textual_indication=None, custom_markup=None, decimal=False, hide=False)

        """
        return self._tempo

    @property
    def time_signature(self) -> abjad.TimeSignature:
        """
        Gets the time signature of the ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=abjad.Offset(1000),
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ... )

            >>> q_target_measure.time_signature
            TimeSignature(pair=(4, 4), hide=False, partial=None)

        """
        return self._time_signature

    @property
    def use_full_measure(self) -> bool:
        """
        Is true when ``QTargetMeasure`` uses full measures:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=abjad.Offset(1000),
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ... )

            >>> q_target_measure.use_full_measure
            False

        """
        return self._use_full_measure
