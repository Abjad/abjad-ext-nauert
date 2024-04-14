import collections
import copy
import itertools
import numbers
import typing

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
        ...     q_event
        ...
        PitchedQEvent(offset=Offset((0, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        SilentQEvent(offset=Offset((1000, 1)), index=None, attachments=())
        PitchedQEvent(offset=Offset((1500, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        SilentQEvent(offset=Offset((2750, 1)), index=None, attachments=())
        PitchedQEvent(offset=Offset((3250, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        TerminalQEvent(offset=Offset((4000, 1)), index=None, attachments=())

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_sequence",)

    ### INITIALIZER ###

    def __init__(self, sequence):
        q_event_classes = (PitchedQEvent, SilentQEvent)
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
            offset_sequence = list(offsets)
            assert abjad.sequence.is_increasing(offset_sequence, strict=False)
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
        if type(self) is type(argument):
            if self.sequence == argument.sequence:
                return True
        return False

    @typing.overload
    def __getitem__(self, argument: int) -> QEvent:
        pass

    @typing.overload
    def __getitem__(self, argument: slice) -> tuple[QEvent, ...]:
        pass

    def __getitem__(self, argument: int | slice) -> QEvent | tuple[QEvent, ...]:
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
    def sequence(self) -> tuple:
        r"""
        Sequence of q-events.

        >>> durations = (1000, -500, 1250, -500, 750)
        >>> sequence = nauert.QEventSequence.from_millisecond_durations(
        ...     durations)

        >>> for q_event in sequence.sequence:
        ...     q_event
        ...
        PitchedQEvent(offset=Offset((0, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        SilentQEvent(offset=Offset((1000, 1)), index=None, attachments=())
        PitchedQEvent(offset=Offset((1500, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        SilentQEvent(offset=Offset((2750, 1)), index=None, attachments=())
        PitchedQEvent(offset=Offset((3250, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        TerminalQEvent(offset=Offset((4000, 1)), index=None, attachments=())

        """
        return self._sequence

    ### PUBLIC METHODS ###

    @classmethod
    def from_millisecond_durations(
        class_,
        milliseconds: typing.Sequence[int | float],
        fuse_silences: bool = False,
    ) -> "QEventSequence":
        r"""
        Changes sequence of millisecond durations ``durations`` to a ``QEventSequence``:

        >>> durations = [-250, 500, -1000, 1250, -1000]
        >>> sequence = nauert.QEventSequence.from_millisecond_durations(
        ...     durations)

        >>> for q_event in sequence:
        ...     q_event
        ...
        SilentQEvent(offset=Offset((0, 1)), index=None, attachments=())
        PitchedQEvent(offset=Offset((250, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        SilentQEvent(offset=Offset((750, 1)), index=None, attachments=())
        PitchedQEvent(offset=Offset((1750, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        SilentQEvent(offset=Offset((3000, 1)), index=None, attachments=())
        TerminalQEvent(offset=Offset((4000, 1)), index=None, attachments=())

        """
        durations: typing.Sequence[int | float]
        if fuse_silences:
            durations = [
                _ for _ in abjad.sequence.sum_by_sign(milliseconds, sign=[-1]) if _
            ]
        else:
            durations = milliseconds
        offsets = abjad.math.cumulative_sums([abs(_) for _ in durations])
        q_events: list[QEvent] = []
        for offset, duration in zip(offsets, durations):
            offset = abjad.Offset(offset)
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
        class_, offsets: typing.Sequence[abjad.typings.Offset]
    ) -> "QEventSequence":
        r"""
        Changes millisecond offsets ``offsets`` to a ``QEventSequence``:

        >>> offsets = [0, 250, 750, 1750, 3000, 4000]
        >>> sequence = nauert.QEventSequence.from_millisecond_offsets(
        ...     offsets)

        >>> for q_event in sequence:
        ...     q_event
        ...
        PitchedQEvent(offset=Offset((0, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        PitchedQEvent(offset=Offset((250, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        PitchedQEvent(offset=Offset((750, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        PitchedQEvent(offset=Offset((1750, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        PitchedQEvent(offset=Offset((3000, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        TerminalQEvent(offset=Offset((4000, 1)), index=None, attachments=())

        """
        q_events: list[QEvent] = []
        q_events.extend([PitchedQEvent(_, [0]) for _ in offsets[:-1]])
        q_events.append(TerminalQEvent(offsets[-1]))
        return class_(q_events)

    @classmethod
    def from_millisecond_pitch_attachment_tuples(
        class_, tuples: typing.Iterable[tuple]
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
        ...     q_event
        ...
        PitchedQEvent(offset=Offset((0, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=('foo',))
        SilentQEvent(offset=Offset((250, 1)), index=None, attachments=())
        PitchedQEvent(offset=Offset((750, 1)), pitches=(NamedPitch("d'"), NamedPitch("ef'")), index=None, attachments=())
        SilentQEvent(offset=Offset((1750, 1)), index=None, attachments=())
        PitchedQEvent(offset=Offset((3000, 1)), pitches=(NamedPitch("cs'"),), index=None, attachments=('foobar', 'foo'))
        TerminalQEvent(offset=Offset((4000, 1)), index=None, attachments=())

        """
        assert isinstance(tuples, collections.abc.Iterable)
        assert all(isinstance(_, collections.abc.Iterable) for _ in tuples)
        assert all(len(_) == 3 for _ in tuples)
        assert all(0 < duration for duration, _, _ in tuples)
        for _, pitches, attachments in tuples:
            assert isinstance(
                pitches, numbers.Number | type(None) | collections.abc.Sequence
            )
            if isinstance(pitches, collections.abc.Sequence):
                assert 0 < len(pitches)
                assert all(isinstance(_, numbers.Number) for _ in pitches)
            if pitches is None:
                assert attachments is None
        # fuse silences
        g = itertools.groupby(tuples, lambda _: _[1] is not None)
        groups = []
        for value, group in g:
            if value:
                groups.extend(list(group))
            else:
                duration = sum(_[0] for _ in group)
                groups.append((duration, None, None))
        # find offsets
        offsets = abjad.math.cumulative_sums([abs(_[0]) for _ in groups])
        offsets = [abjad.Offset(_) for _ in offsets]
        # build QEvents
        q_events = [
            QEvent.from_offset_pitches_attachments(offset, pitches, attachments)
            for offset, (_, pitches, attachments) in zip(offsets, groups)
        ]
        q_events.append(TerminalQEvent(offsets[-1]))
        return class_(q_events)

    @classmethod
    def from_millisecond_pitch_pairs(
        class_, pairs: typing.Iterable[tuple]
    ) -> "QEventSequence":
        r"""
        Changes millisecond-duration:pitch pairs ``pairs`` into a ``QEventSequence``:

        >>> durations = [250, 500, 1000, 1250, 1000]
        >>> pitches = [(0,), None, (2, 3), None, (1,)]
        >>> pairs = tuple(zip(durations, pitches))
        >>> sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(
        ...     pairs)

        >>> for q_event in sequence:
        ...     q_event
        ...
        PitchedQEvent(offset=Offset((0, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        SilentQEvent(offset=Offset((250, 1)), index=None, attachments=())
        PitchedQEvent(offset=Offset((750, 1)), pitches=(NamedPitch("d'"), NamedPitch("ef'")), index=None, attachments=())
        SilentQEvent(offset=Offset((1750, 1)), index=None, attachments=())
        PitchedQEvent(offset=Offset((3000, 1)), pitches=(NamedPitch("cs'"),), index=None, attachments=())
        TerminalQEvent(offset=Offset((4000, 1)), index=None, attachments=())

        """
        assert isinstance(pairs, collections.abc.Iterable)
        assert all(isinstance(_, collections.abc.Iterable) for _ in pairs)
        assert all(len(_) == 2 for _ in pairs)
        assert all(0 < duration for duration, _ in pairs)
        for _, pitches in pairs:
            assert isinstance(
                pitches, (numbers.Number, type(None), collections.abc.Sequence)
            )
            if isinstance(pitches, collections.abc.Sequence):
                assert 0 < len(pitches)
                assert all(isinstance(_, numbers.Number) for _ in pitches)
        return class_.from_millisecond_pitch_attachment_tuples(
            [(duration, pitches, None) for duration, pitches in pairs]
        )

    @classmethod
    def from_tempo_scaled_durations(
        class_,
        durations: typing.Sequence[abjad.typings.Duration],
        tempo: abjad.MetronomeMark,
    ) -> "QEventSequence":
        r"""
        Changes ``durations``, scaled by ``tempo`` into a ``QEventSequence``:

        ..  container:: example

            >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 174)
            >>> durations = [(1, 4), (-3, 16), (1, 16), (-1, 2)]
            >>> sequence = nauert.QEventSequence.from_tempo_scaled_durations(
            ...     durations, tempo=tempo)

            >>> for q_event in sequence:
            ...     q_event
            ...
            PitchedQEvent(offset=Offset((0, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
            SilentQEvent(offset=Offset((10000, 29)), index=None, attachments=())
            PitchedQEvent(offset=Offset((17500, 29)), pitches=(NamedPitch("c'"),), index=None, attachments=())
            SilentQEvent(offset=Offset((20000, 29)), index=None, attachments=())
            TerminalQEvent(offset=Offset((40000, 29)), index=None, attachments=())

        """
        durations = [abjad.Duration(x) for x in durations]
        assert isinstance(tempo, abjad.MetronomeMark)
        durations = [x for x in abjad.sequence.sum_by_sign(durations, sign=[-1]) if x]
        durations = [tempo.duration_to_milliseconds(_) for _ in durations]
        offsets = abjad.math.cumulative_sums([abs(_) for _ in durations])
        q_events = []
        for offset, duration in zip(offsets, durations):
            offset = abjad.Offset(offset)
            assert isinstance(duration, abjad.Duration)
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
    def from_tempo_scaled_leaves(class_, leaves, tempo=None) -> "QEventSequence":
        r"""
        Changes ``leaves``, optionally with ``tempo`` into a ``QEventSequence``:

        >>> staff = abjad.Staff("c'4 <d' fs'>8. r16 gqs'2")
        >>> tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 72)
        >>> sequence = nauert.QEventSequence.from_tempo_scaled_leaves(staff[:], tempo)
        >>> for q_event in sequence:
        ...     q_event
        ...
        PitchedQEvent(offset=Offset((0, 1)), pitches=(NamedPitch("c'"),), index=None, attachments=())
        PitchedQEvent(offset=Offset((2500, 3)), pitches=(NamedPitch("d'"), NamedPitch("fs'")), index=None, attachments=())
        SilentQEvent(offset=Offset((4375, 3)), index=None, attachments=())
        PitchedQEvent(offset=Offset((5000, 3)), pitches=(NamedPitch("gqs'"),), index=None, attachments=())
        TerminalQEvent(offset=Offset((10000, 3)), index=None, attachments=())

        If ``tempo`` is ``None``, all leaves in ``leaves`` must have an
        effective, non-imprecise tempo. The millisecond-duration of each leaf
        will be determined by its effective tempo.
        """
        assert len(leaves)
        match tempo:
            case None:
                prototype = abjad.MetronomeMark
                assert abjad.get.effective(leaves[0], prototype) is not None
            case abjad.MetronomeMark():
                tempo = copy.deepcopy(tempo)
            case tuple():
                tempo = abjad.MetronomeMark(*tempo)
            case _:
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
                    rgroup, lambda x: abjad._iterlib._get_logical_tie_leaves(x)
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
            pitch: typing.Any
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
