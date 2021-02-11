import typing

import abjad

from .qeventproxy import QEventProxy
from .qevents import QEvent
from .qgrid import QGrid
from .quantizationjob import QuantizationJob
from .searchtrees import SearchTree, UnweightedSearchTree


class QTargetBeat:
    """
    Q-target beat.

    Represents a single beat in a quantization target.

    ..  container:: example

        >>> beatspan = (1, 8)
        >>> offset_in_ms = 1500
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark((1, 4), 56)

        >>> q_target_beat = nauert.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ... )

        >>> string = abjad.storage(q_target_beat)
        >>> print(string)
        nauert.QTargetBeat(
            beatspan=abjad.Duration(1, 8),
            offset_in_ms=abjad.Offset((1500, 1)),
            search_tree=nauert.UnweightedSearchTree(
                definition={   3: None,
                    },
                ),
            tempo=abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 4),
                units_per_minute=56,
                ),
            )

    Not composer-safe.

    Used internally by ``Quantizer``.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_beatspan",
        "_distances",
        "_grouping",
        "_offset_in_ms",
        "_q_events",
        "_q_grid",
        "_q_grids",
        "_search_tree",
        "_tempo",
    )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, beatspan=None, offset_in_ms=None, search_tree=None, tempo=None):
        beatspan = beatspan or abjad.Duration(0)
        beatspan = abjad.Duration(beatspan)
        offset_in_ms = offset_in_ms or abjad.Duration(0)
        offset_in_ms = abjad.Offset(offset_in_ms)

        if search_tree is None:
            search_tree = UnweightedSearchTree()
        assert isinstance(search_tree, SearchTree)
        tempo = tempo or abjad.MetronomeMark((1, 4), 60)
        # tempo = abjad.MetronomeMark(tempo)
        if isinstance(tempo, tuple):
            tempo = abjad.MetronomeMark(*tempo)
        assert not tempo.is_imprecise

        q_events = []
        q_grids = []

        self._beatspan = beatspan
        self._distances = {}
        self._offset_in_ms = offset_in_ms
        self._q_events = q_events
        self._q_grid = None
        self._q_grids = q_grids
        self._search_tree = search_tree
        self._tempo = tempo

    ### SPECIAL METHODS ###

    def __call__(self, job_id):
        """
        Calls q-target beat.

        Returns quantization job.
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

    def __format__(self, format_specification="") -> str:
        """
        Formats q-event.

        Set `format_specification` to `''` or `'storage'`. Interprets `''`
        equal to `'storage'`.
        """
        if format_specification in ("", "storage"):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self) -> abjad.Duration:
        """
        Beatspan of q-target beat.

        >>> beatspan = (1, 8)
        >>> offset_in_ms = 1500
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark((1, 4), 56)

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
    def distances(self) -> typing.Tuple:
        """
        A list of computed distances between the ``QEventProxies``
        associated with a ``QTargetBeat`` instance, and each ``QGrid``
        generated for that beat.

        Used internally by the ``Quantizer``.
        """
        return self._distances

    @property
    def duration_in_ms(self) -> abjad.Duration:
        """
        Duration in milliseconds of the q-target beat.

        >>> beatspan = (1, 8)
        >>> offset_in_ms = 1500
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark((1, 4), 56)

        >>> q_target_beat = nauert.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     )

        >>> q_target_beat.duration_in_ms
        Duration(3750, 7)

        """
        return self.tempo.duration_to_milliseconds(self.beatspan)

    @property
    def offset_in_ms(self) -> abjad.Offset:
        """
        Offset in milliseconds of q-target beat.

        >>> beatspan = (1, 8)
        >>> offset_in_ms = 1500
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark((1, 4), 56)

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
    def q_events(self) -> typing.List:
        """
        A list for storing ``QEventProxy`` instances.

        Used internally by the ``Quantizer``.
        """
        return self._q_events

    @property
    def q_grid(self) -> QGrid:
        """
        The ``QGrid`` instance selected by a ``Heuristic``.

        Used internally by the ``Quantizer``.
        """
        return self._q_grid

    @property
    def q_grids(self) -> typing.Tuple:
        """
        A tuple of ``QGrids`` generated by a ``QuantizationJob``.

        Used internally by the ``Quantizer``.
        """
        return self._q_grids

    @property
    def search_tree(self):
        """
        Search tree of q-target beat.

        >>> beatspan = (1, 8)
        >>> offset_in_ms = 1500
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark((1, 4), 56)

        >>> q_target_beat = nauert.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     )

        >>> q_target_beat.search_tree
        UnweightedSearchTree(definition={3: None})

        Returns search tree.
        """
        return self._search_tree

    @property
    def tempo(self) -> abjad.MetronomeMark:
        """
        MetronomeMark of q-target beat.

        >>> beatspan = (1, 8)
        >>> offset_in_ms = 1500
        >>> search_tree = nauert.UnweightedSearchTree({3: None})
        >>> tempo = abjad.MetronomeMark((1, 4), 56)

        >>> q_target_beat = nauert.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     )

        >>> q_target_beat.tempo
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=56)

        """
        return self._tempo


class QTargetMeasure:
    """
    Q-target measure.

    Represents a single measure in a measurewise quantization target.

    ..  container:: example

        >>> search_tree = nauert.UnweightedSearchTree({2: None})
        >>> tempo = abjad.MetronomeMark((1, 4), 60)
        >>> time_signature = abjad.TimeSignature((4, 4))

        >>> q_target_measure = nauert.QTargetMeasure(
        ...     offset_in_ms=1000,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     time_signature=time_signature,
        ... )

        >>> string = abjad.storage(q_target_measure)
        >>> print(string)
        nauert.QTargetMeasure(
            offset_in_ms=abjad.Offset((1000, 1)),
            search_tree=nauert.UnweightedSearchTree(
                definition={   2: None,
                    },
                ),
            time_signature=abjad.TimeSignature((4, 4)),
            tempo=abjad.MetronomeMark(
                reference_duration=abjad.Duration(1, 4),
                units_per_minute=60,
                ),
            use_full_measure=False,
            )

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
        ...     offset_in_ms=1000,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     time_signature=time_signature,
        ...     use_full_measure=True,
        ... )

        >>> for q_target_beat in another_q_target_measure.beats:
        ...     print(q_target_beat.offset_in_ms, q_target_beat.duration_in_ms)
        1000 4000

    Not composer-safe.

    Used internally by ``Quantizer``.
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

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        offset_in_ms=None,
        search_tree=None,
        time_signature=None,
        tempo=None,
        use_full_measure=False,
    ):
        offset_in_ms = offset_in_ms or 0
        offset_in_ms = abjad.Offset(offset_in_ms)

        if search_tree is None:
            search_tree = UnweightedSearchTree()
        assert isinstance(search_tree, SearchTree)
        tempo = tempo or abjad.MetronomeMark((1, 4), 60)
        # tempo = abjad.MetronomeMark(tempo)
        if isinstance(tempo, tuple):
            tempo = abjad.MetronomeMark(*tempo)
        assert not tempo.is_imprecise
        time_signature = time_signature or (4, 4)
        time_signature = abjad.TimeSignature(time_signature)
        use_full_measure = bool(use_full_measure)

        beats = []

        if use_full_measure:
            beatspan = time_signature.duration
            beat = QTargetBeat(
                beatspan=beatspan,
                offset_in_ms=offset_in_ms,
                search_tree=search_tree,
                tempo=tempo,
            )
            beats.append(beat)
        else:
            beatspan = abjad.Duration(1, time_signature.denominator)
            current_offset_in_ms = offset_in_ms
            beatspan_duration_in_ms = tempo.duration_to_milliseconds(beatspan)
            for i in range(time_signature.numerator):
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
        self._time_signature = time_signature
        self._use_full_measure = use_full_measure

    ### SPECIAL METHODS ###

    def __format__(self, format_specification="") -> str:
        """
        Formats q-event.

        Set `format_specification` to `''` or `'storage'`. Interprets `''`
        equal to `'storage'`.
        """
        if format_specification in ("", "storage"):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self) -> typing.Tuple:
        """
        Gets the tuple of ``QTargetBeats`` contained by the
        ``QTargetMeasure``.

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark((1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=1000,
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ...     )

            >>> for q_target_beat in q_target_measure.beats:
            ...     string = abjad.storage(q_target_beat)
            ...     print(string)
            ...
            nauert.QTargetBeat(
                beatspan=abjad.Duration(1, 4),
                offset_in_ms=abjad.Offset((1000, 1)),
                search_tree=nauert.UnweightedSearchTree(
                    definition={   2: None,
                        },
                    ),
                tempo=abjad.MetronomeMark(
                    reference_duration=abjad.Duration(1, 4),
                    units_per_minute=60,
                    ),
                )
            nauert.QTargetBeat(
                beatspan=abjad.Duration(1, 4),
                offset_in_ms=abjad.Offset((2000, 1)),
                search_tree=nauert.UnweightedSearchTree(
                    definition={   2: None,
                        },
                    ),
                tempo=abjad.MetronomeMark(
                    reference_duration=abjad.Duration(1, 4),
                    units_per_minute=60,
                    ),
                )
            nauert.QTargetBeat(
                beatspan=abjad.Duration(1, 4),
                offset_in_ms=abjad.Offset((3000, 1)),
                search_tree=nauert.UnweightedSearchTree(
                    definition={   2: None,
                        },
                    ),
                tempo=abjad.MetronomeMark(
                    reference_duration=abjad.Duration(1, 4),
                    units_per_minute=60,
                    ),
                )
            nauert.QTargetBeat(
                beatspan=abjad.Duration(1, 4),
                offset_in_ms=abjad.Offset((4000, 1)),
                search_tree=nauert.UnweightedSearchTree(
                    definition={   2: None,
                        },
                    ),
                tempo=abjad.MetronomeMark(
                    reference_duration=abjad.Duration(1, 4),
                    units_per_minute=60,
                    ),
                )

        """
        return self._beats

    @property
    def duration_in_ms(self) -> abjad.Duration:
        """
        The duration in milliseconds of the ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark((1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=1000,
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ...     )

            >>> q_target_measure.duration_in_ms
            Duration(4000, 1)

        """
        return self.tempo.duration_to_milliseconds(self.time_signature.duration)

    @property
    def offset_in_ms(self) -> abjad.Offset:
        """
        The offset in milliseconds of the ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark((1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=1000,
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ...     )

            >>> q_target_measure.offset_in_ms
            Offset((1000, 1))

        """
        return self._offset_in_ms

    @property
    def search_tree(self) -> UnweightedSearchTree:
        """
        The search tree of the ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark((1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=1000,
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ...     )

            >>> q_target_measure.search_tree
            UnweightedSearchTree(definition={2: None})

        """
        return self._search_tree

    @property
    def tempo(self) -> abjad.MetronomeMark:
        """
        The tempo of the ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark((1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=1000,
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ...     )

            >>> q_target_measure.tempo
            MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=60)

        """
        return self._tempo

    @property
    def time_signature(self) -> abjad.TimeSignature:
        """
        The time signature of the ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark((1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=1000,
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ...     )

            >>> q_target_measure.time_signature
            TimeSignature((4, 4))

        """
        return self._time_signature

    @property
    def use_full_measure(self) -> bool:
        """
        The ``use_full_measure`` flag of the ``QTargetMeasure``:

        ..  container:: example

            >>> search_tree = nauert.UnweightedSearchTree({2: None})
            >>> tempo = abjad.MetronomeMark((1, 4), 60)
            >>> time_signature = abjad.TimeSignature((4, 4))

            >>> q_target_measure = nauert.QTargetMeasure(
            ...     offset_in_ms=1000,
            ...     search_tree=search_tree,
            ...     tempo=tempo,
            ...     time_signature=time_signature,
            ...     )

            >>> q_target_measure.use_full_measure
            False

        """
        return self._use_full_measure
