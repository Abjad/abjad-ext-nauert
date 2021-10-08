import collections
import copy
import itertools
import numbers
import typing

import quicktions

import abjad

from .qevents import PitchedQEvent, QEvent, SilentQEvent, TerminalQEvent


class QEventSequence:
    r"""
    Q-event sequence.

    Contains only pitched q-events and silent q-events, and terminates with a
    single terminal q-event.

    A q-event sequence is the primary input to the quantizer.

    ..  container:: example

        A q-event sequence provides a number of convenience functions to assist
        with instantiating new sequences:

        >>> durations = (1000, -500, 1250, -500, 750)
        >>> sequence = nauert.QEventSequence.from_millisecond_durations(
        ...     durations
        ... )

        >>> for q_event in sequence:
        ...     string = abjad.storage(q_event)
        ...     print(string)
        ...
        nauert.PitchedQEvent(
            offset=abjad.Offset((0, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((1000, 1)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((1500, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((2750, 1)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((3250, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.TerminalQEvent(
            offset=abjad.Offset((4000, 1)),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_sequence",)

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        sequence: typing.Optional[
            typing.Union["QEventSequence", typing.Sequence[QEvent]]
        ] = None,
    ):

        q_event_classes = (
            PitchedQEvent,
            SilentQEvent,
        )
        self._sequence: typing.Tuple[QEvent, ...]
        if sequence is None:
            self._sequence = ()
            return
        else:
            assert 1 < len(sequence)
            assert all(
                isinstance(q_event, q_event_classes) for q_event in sequence[:-1]
            )
            assert isinstance(sequence[-1], TerminalQEvent)
            offsets = [x.offset for x in sequence]
            offset_sequence = abjad.Sequence(offsets)
            assert offset_sequence.is_increasing(strict=False)
            assert 0 <= sequence[0].offset
            self._sequence = tuple(sequence)

    ### SPECIAL METHODS ###

    def __contains__(self, argument) -> bool:
        """
        Is true when q-event sequence contains ``argument``. Otherwise false.
        """
        return argument in self._sequence

    def __eq__(self, argument) -> bool:
        """
        Is true when q-event sequence equals ``argument``. Otherwise false.
        """
        if type(self) == type(argument):
            if self.sequence == argument.sequence:
                return True
        return False

    def __format__(self, format_specification: str = "") -> str:
        r"""
        Formats q-event sequence.

        Set ``format_specification`` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        >>> durations = (1000, -500, 1250, -500, 750)
        >>> sequence = nauert.QEventSequence.from_millisecond_durations(
        ...     durations)

        >>> string = format(sequence)
        >>> print(string)
        nauert.QEventSequence(
            (
                nauert.PitchedQEvent(
                    offset=abjad.Offset((0, 1)),
                    pitches=(
                        abjad.NamedPitch("c'"),
                        ),
                    ),
                nauert.SilentQEvent(
                    offset=abjad.Offset((1000, 1)),
                    ),
                nauert.PitchedQEvent(
                    offset=abjad.Offset((1500, 1)),
                    pitches=(
                        abjad.NamedPitch("c'"),
                        ),
                    ),
                nauert.SilentQEvent(
                    offset=abjad.Offset((2750, 1)),
                    ),
                nauert.PitchedQEvent(
                    offset=abjad.Offset((3250, 1)),
                    pitches=(
                        abjad.NamedPitch("c'"),
                        ),
                    ),
                nauert.TerminalQEvent(
                    offset=abjad.Offset((4000, 1)),
                    ),
                )
            )

        """
        if format_specification in ("", "storage"):
            return abjad.storage(self)
        return str(self)

    @typing.overload
    def __getitem__(self, argument: int) -> QEvent:
        ...

    @typing.overload
    def __getitem__(self, argument: slice) -> typing.Tuple[QEvent, ...]:
        ...

    def __getitem__(
        self, argument: typing.Union[int, slice]
    ) -> typing.Union[QEvent, typing.Tuple[QEvent, ...]]:
        """
        Gets item or slice identified by `argument`.

        Returns item or slice.
        """
        return self._sequence.__getitem__(argument)

    def __hash__(self) -> int:
        """
        Hashes q-event sequence.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        return super(QEventSequence, self).__hash__()

    def __iter__(self) -> typing.Iterator[QEvent]:
        """
        Iterates q-event sequence.

        Yields items.
        """
        for x in self._sequence:
            yield x

    def __len__(self) -> int:
        """
        Length of q-event sequence.
        """
        return len(self._sequence)

    ### PRIVATE METHODS ###

    def _get_format_specification(self) -> abjad.FormatSpecification:
        values = []
        if self.sequence:
            values.append(self.sequence)
        return abjad.FormatSpecification(
            storage_format_args_values=tuple(values),
            storage_format_keyword_names=None,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def duration_in_ms(self) -> abjad.Duration:
        r"""
        Duration in milliseconds of the ``QEventSequence``:

        >>> durations = (1000, -500, 1250, -500, 750)
        >>> sequence = nauert.QEventSequence.from_millisecond_durations(
        ...     durations)

        >>> sequence.duration_in_ms
        Duration(4000, 1)

        """
        return abjad.Duration(self[-1].offset)

    @property
    def sequence(self) -> typing.Tuple:
        r"""
        Sequence of q-events.

        >>> durations = (1000, -500, 1250, -500, 750)
        >>> sequence = nauert.QEventSequence.from_millisecond_durations(
        ...     durations)

        >>> for q_event in sequence.sequence:
        ...     string = abjad.storage(q_event)
        ...     print(string)
        ...
        nauert.PitchedQEvent(
            offset=abjad.Offset((0, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((1000, 1)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((1500, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((2750, 1)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((3250, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.TerminalQEvent(
            offset=abjad.Offset((4000, 1)),
            )

        """
        return self._sequence

    ### PUBLIC METHODS ###

    @classmethod
    def from_millisecond_durations(
        class_,
        milliseconds: typing.Union[typing.Sequence[abjad.typings.Number]],
        fuse_silences: bool = False,
    ) -> "QEventSequence":
        r"""
        Changes sequence of millisecond durations ``durations`` to a ``QEventSequence``:

        >>> durations = [-250, 500, -1000, 1250, -1000]
        >>> sequence = nauert.QEventSequence.from_millisecond_durations(
        ...     durations)

        >>> for q_event in sequence:
        ...     string = abjad.storage(q_event)
        ...     print(string)
        ...
        nauert.SilentQEvent(
            offset=abjad.Offset((0, 1)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((250, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((750, 1)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((1750, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((3000, 1)),
            )
        nauert.TerminalQEvent(
            offset=abjad.Offset((4000, 1)),
            )

        """
        durations: typing.Union[
            typing.Sequence[numbers.Real], typing.Sequence[abjad.typings.Number]
        ]
        if fuse_silences:
            durations = [
                x for x in abjad.Sequence(milliseconds).sum_by_sign(sign=[-1]) if x
            ]
        else:
            durations = milliseconds
        offsets = abjad.math.cumulative_sums([abs(x) for x in durations])
        q_events: typing.List[QEvent] = []
        for pair in zip(offsets, durations):
            offset = abjad.Offset(pair[0])
            duration = pair[1]
            q_event: QEvent
            # negative duration indicates silence
            if duration < 0:
                q_event = SilentQEvent(offset)
            else:
                q_event = PitchedQEvent(offset, [0])
            q_events.append(q_event)
        q_events.append(TerminalQEvent(abjad.Offset(offsets[-1])))
        return class_(q_events)

    @classmethod
    def from_millisecond_offsets(
        class_,
        offsets: typing.Union[
            typing.Sequence[numbers.Real], typing.Sequence[abjad.typings.Number]
        ],
    ) -> "QEventSequence":
        r"""
        Changes millisecond offsets ``offsets`` to a ``QEventSequence``:

        >>> offsets = [0, 250, 750, 1750, 3000, 4000]
        >>> sequence = nauert.QEventSequence.from_millisecond_offsets(
        ...     offsets)

        >>> for q_event in sequence:
        ...     string = abjad.storage(q_event)
        ...     print(string)
        ...
        nauert.PitchedQEvent(
            offset=abjad.Offset((0, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((250, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((750, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((1750, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((3000, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.TerminalQEvent(
            offset=abjad.Offset((4000, 1)),
            )

        """
        q_events: typing.List[QEvent] = []
        q_events.extend([PitchedQEvent(x, [0]) for x in offsets[:-1]])
        q_events.append(TerminalQEvent(offsets[-1]))
        return class_(q_events)

    @classmethod
    def from_millisecond_pitch_attachment_tuples(
        class_,
        tuples: typing.Iterable[
            typing.Tuple[
                abjad.typings.Number,
                typing.Optional[typing.Tuple[abjad.typings.Number, ...]],
                typing.Optional[tuple],
            ]
        ],
    ) -> "QEventSequence":
        r"""
        Changes millisecond-duration:pitch:attachment tuples ``tuples`` into a ``QEventSequence``:

        >>> durations = [250, 500, 1000, 1250, 1000]
        >>> pitches = [(0,), None, (2, 3), None, (1,)]
        >>> attachments = [("foo",), None, None, None, ("foobar", "foo")]
        >>> tuples = tuple(zip(durations, pitches, attachments))
        >>> sequence = nauert.QEventSequence.from_millisecond_pitch_attachment_tuples(
        ...     tuples
        ... )
        >>> for q_event in sequence:
        ...     string = abjad.storage(q_event)
        ...     print(string)
        ...
        nauert.PitchedQEvent(
            offset=abjad.Offset((0, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            attachments=('foo',),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((250, 1)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((750, 1)),
            pitches=(
                abjad.NamedPitch("d'"),
                abjad.NamedPitch("ef'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((1750, 1)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((3000, 1)),
            pitches=(
                abjad.NamedPitch("cs'"),
                ),
            attachments=('foobar', 'foo'),
            )
        nauert.TerminalQEvent(
            offset=abjad.Offset((4000, 1)),
            )

        """
        assert isinstance(tuples, collections.abc.Iterable)
        assert all(isinstance(x, collections.abc.Iterable) for x in tuples)
        assert all(len(x) == 3 for x in tuples)
        assert all(0 < x[0] for x in tuples)
        for tuple_ in tuples:
            assert isinstance(
                tuple_[1], (numbers.Number, type(None), collections.abc.Sequence)
            )
            if isinstance(tuple_[1], collections.abc.Sequence):
                assert 0 < len(tuple_[1])
                assert all(isinstance(x, numbers.Number) for x in tuple_[1])
            if tuple_[1] is None:
                assert tuple_[2] is None
        # fuse silences
        g = itertools.groupby(tuples, lambda x: x[1] is not None)
        groups = []
        for value, group in g:
            if value:
                groups.extend(list(group))
            else:
                duration = sum(x[0] for x in group)
                groups.append((duration, None, None))
        # find offsets
        offsets = abjad.math.cumulative_sums([abs(x[0]) for x in groups])
        # build QEvents
        q_events: typing.List[QEvent] = []
        for pair in zip(offsets, groups):
            offset = abjad.Offset(pair[0])
            pitches = pair[1][1]
            attachments = pair[1][2]
            if isinstance(pitches, collections.abc.Iterable):
                assert all(isinstance(x, numbers.Number) for x in pitches)
                q_events.append(PitchedQEvent(offset, pitches, attachments))
            elif isinstance(pitches, type(None)):
                q_events.append(SilentQEvent(offset))
            elif isinstance(pitches, numbers.Number):
                q_events.append(PitchedQEvent(offset, [pitches], attachments))
        q_events.append(TerminalQEvent(abjad.Offset(offsets[-1])))
        return class_(q_events)

    @classmethod
    def from_millisecond_pitch_pairs(
        class_,
        pairs: typing.Iterable[
            typing.Tuple[
                abjad.typings.Number,
                typing.Optional[
                    typing.Union[
                        abjad.typings.Number, typing.Tuple[abjad.typings.Number, ...]
                    ]
                ],
            ]
        ],
    ) -> "QEventSequence":
        r"""
        Changes millisecond-duration:pitch pairs ``pairs`` into a ``QEventSequence``:

        >>> durations = [250, 500, 1000, 1250, 1000]
        >>> pitches = [(0,), None, (2, 3), None, (1,)]
        >>> pairs = tuple(zip(durations, pitches))
        >>> sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        ...     pairs)

        >>> for q_event in sequence:
        ...     string = abjad.storage(q_event)
        ...     print(string)
        ...
        nauert.PitchedQEvent(
            offset=abjad.Offset((0, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((250, 1)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((750, 1)),
            pitches=(
                abjad.NamedPitch("d'"),
                abjad.NamedPitch("ef'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((1750, 1)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((3000, 1)),
            pitches=(
                abjad.NamedPitch("cs'"),
                ),
            )
        nauert.TerminalQEvent(
            offset=abjad.Offset((4000, 1)),
            )

        """
        assert isinstance(pairs, collections.abc.Iterable)
        assert all(isinstance(x, collections.abc.Iterable) for x in pairs)
        assert all(len(x) == 2 for x in pairs)
        assert all(0 < x[0] for x in pairs)
        for _, pitches in pairs:
            assert isinstance(
                pitches, (numbers.Number, type(None), collections.abc.Sequence)
            )
            if isinstance(pitches, collections.abc.Sequence):
                assert 0 < len(pitches)
                assert all(isinstance(x, numbers.Number) for x in pitches)
        # fuse silences
        g = itertools.groupby(pairs, lambda x: x[1] is not None)
        groups = []
        for value, group in g:
            if value:
                groups.extend(list(group))
            else:
                duration = sum(x[0] for x in group)
                groups.append((duration, None))
        # find offsets
        offsets = abjad.math.cumulative_sums([abs(x[0]) for x in groups])
        # build QEvents
        q_events: typing.List[QEvent] = []
        for pair in zip(offsets, groups):
            offset = abjad.Offset(pair[0])
            pitches = pair[1][1]
            if isinstance(pitches, collections.abc.Iterable):
                assert all(isinstance(x, numbers.Number) for x in pitches)
                q_events.append(PitchedQEvent(offset, pitches))
            elif isinstance(pitches, type(None)):
                q_events.append(SilentQEvent(offset))
            elif isinstance(pitches, numbers.Number):
                q_events.append(PitchedQEvent(offset, [pitches]))
        q_events.append(TerminalQEvent(abjad.Offset(offsets[-1])))
        return class_(q_events)

    @classmethod
    def from_tempo_scaled_durations(
        class_,
        durations: abjad.typings.DurationSequenceTyping,
        tempo: abjad.MetronomeMark,
    ) -> "QEventSequence":
        r"""
        Changes ``durations``, scaled by ``tempo`` into a ``QEventSequence``:

        >>> tempo = abjad.MetronomeMark((1, 4), 174)
        >>> durations = [(1, 4), (-3, 16), (1, 16), (-1, 2)]
        >>> sequence = nauert.QEventSequence.from_tempo_scaled_durations(
        ...     durations, tempo=tempo)

        >>> for q_event in sequence:
        ...     string = abjad.storage(q_event)
        ...     print(string)
        ...
        nauert.PitchedQEvent(
            offset=abjad.Offset((0, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((10000, 29)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((17500, 29)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((20000, 29)),
            )
        nauert.TerminalQEvent(
            offset=abjad.Offset((40000, 29)),
            )

        """
        durations = [abjad.Duration(x) for x in durations]
        assert isinstance(tempo, abjad.MetronomeMark)
        durations = [x for x in abjad.Sequence(durations).sum_by_sign(sign=[-1]) if x]
        durations = [tempo.duration_to_milliseconds(_) for _ in durations]
        offsets = abjad.math.cumulative_sums([abs(_) for _ in durations])
        q_events = []
        for pair in zip(offsets, durations):
            offset = abjad.Offset(pair[0])
            assert isinstance(pair[1], abjad.Duration)
            duration: abjad.Duration = pair[1]
            q_event: QEvent
            # negative duration indicates silence
            if duration < 0:
                q_event = SilentQEvent(offset)
            # otherwise use middle C
            else:
                q_event = PitchedQEvent(offset, [0])
            q_events.append(q_event)
        # insert terminating silence QEvent
        q_events.append(TerminalQEvent(offsets[-1]))
        return class_(q_events)

    @classmethod
    def from_tempo_scaled_leaves(
        class_,
        leaves: typing.Union[
            abjad.Selection,
            typing.Sequence[typing.Union[abjad.Component, abjad.Selection]],
        ],
        tempo: typing.Optional[
            typing.Union[
                abjad.MetronomeMark,
                typing.Tuple[
                    abjad.typings.DurationTyping, typing.Union[int, quicktions.Fraction]
                ],
            ]
        ] = None,
    ) -> "QEventSequence":
        r"""
        Changes ``leaves``, optionally with ``tempo`` into a ``QEventSequence``:

        >>> staff = abjad.Staff("c'4 <d' fs'>8. r16 gqs'2")
        >>> tempo = abjad.MetronomeMark((1, 4), 72)
        >>> sequence = nauert.QEventSequence.from_tempo_scaled_leaves(
        ...     staff[:],
        ...     tempo=tempo,
        ... )

        >>> for q_event in sequence:
        ...     string = abjad.storage(q_event)
        ...     print(string)
        ...
        nauert.PitchedQEvent(
            offset=abjad.Offset((0, 1)),
            pitches=(
                abjad.NamedPitch("c'"),
                ),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((2500, 3)),
            pitches=(
                abjad.NamedPitch("d'"),
                abjad.NamedPitch("fs'"),
                ),
            )
        nauert.SilentQEvent(
            offset=abjad.Offset((4375, 3)),
            )
        nauert.PitchedQEvent(
            offset=abjad.Offset((5000, 3)),
            pitches=(
                abjad.NamedPitch("gqs'"),
                ),
            )
        nauert.TerminalQEvent(
            offset=abjad.Offset((10000, 3)),
            )

        If ``tempo`` is ``None``, all leaves in ``leaves`` must have an
        effective, non-imprecise tempo. The millisecond-duration of each leaf
        will be determined by its effective tempo.
        """
        assert abjad.select(leaves).are_contiguous_logical_voice()
        assert len(leaves)
        if tempo is None:
            prototype = abjad.MetronomeMark
            assert abjad.get.effective(leaves[0], prototype) is not None
        elif isinstance(tempo, abjad.MetronomeMark):
            tempo = copy.deepcopy(tempo)
        elif isinstance(tempo, tuple):
            tempo = abjad.MetronomeMark(*tempo)
        else:
            raise TypeError(tempo)
        # sort by silence and tied leaves
        groups = []
        for rvalue, rgroup in itertools.groupby(
            leaves, lambda x: isinstance(x, (abjad.Rest, abjad.Skip))
        ):
            if rvalue:
                groups.append(list(rgroup))
            else:
                for tvalue, tgroup in itertools.groupby(
                    rgroup, lambda x: abjad._iterate._get_logical_tie_leaves(x)
                ):
                    groups.append(list(tgroup))
        # calculate lists of pitches and durations
        durations = []
        pitches = []
        for group in groups:
            # get millisecond cumulative duration
            if tempo is not None:
                duration = sum(
                    tempo.duration_to_milliseconds(x._get_duration()) for x in group
                )
            else:
                duration = sum(
                    abjad.get.effective(
                        x, abjad.MetronomeMark
                    ).duration_to_milliseconds(x._get_duration())
                    for x in group
                )
            durations.append(duration)
            # get pitch of first leaf in group
            if isinstance(group[0], (abjad.Rest, abjad.Skip)):
                pitch = None
            elif isinstance(group[0], abjad.Note):
                assert group[0].written_pitch is not None
                pitch = group[0].written_pitch.number
            # chord
            else:
                pitch = [x.written_pitch.number for x in group[0].note_heads]
            pitches.append(pitch)
        # convert durations and pitches to QEvents and return
        return class_.from_millisecond_pitch_pairs(tuple(zip(durations, pitches)))
