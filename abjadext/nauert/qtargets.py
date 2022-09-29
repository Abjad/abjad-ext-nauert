import abc
import bisect
import copy
import typing

import abjad

from .attackpointoptimizers import (
    AttackPointOptimizer,
    MeasurewiseAttackPointOptimizer,
    NaiveAttackPointOptimizer,
)
from .gracehandlers import ConcatenatingGraceHandler, GraceHandler
from .heuristics import DistanceHeuristic, Heuristic
from .jobhandlers import JobHandler, SerialJobHandler
from .qeventproxy import QEventProxy
from .qevents import TerminalQEvent
from .qeventsequence import QEventSequence
from .qtargetitems import QTargetBeat, QTargetItem, QTargetMeasure


class QTarget(abc.ABC):
    """
    Abstract q-target.

    ``QTarget`` is created by a concrete ``QSchema`` instance, and represents
    the mold into which the timepoints contained by a ``QSequence`` instance
    will be poured, as structured by that ``QSchema`` instance.

    Not composer-safe.

    Used internally by the ``quantize`` function.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_items",)

    ### INITIALIZATION ###

    def __init__(self, items: typing.Sequence[QTargetItem] | None = None):
        items = [] if items is None else items
        assert all(isinstance(x, self.item_class) for x in items)
        self._items: typing.Sequence[QTargetItem] = ()
        if len(items) > 0:
            self._items = tuple(sorted(items, key=lambda x: x.offset_in_ms))

    ### SPECIAL METHODS ###

    def __call__(
        self,
        q_event_sequence: QEventSequence,
        grace_handler: GraceHandler | None = None,
        heuristic: Heuristic | None = None,
        job_handler: JobHandler | None = None,
        attack_point_optimizer: AttackPointOptimizer | None = None,
        attach_tempos: bool = True,
    ):
        """
        Calls q-target.
        """
        assert isinstance(q_event_sequence, QEventSequence)

        if grace_handler is None:
            grace_handler = ConcatenatingGraceHandler()
        assert isinstance(grace_handler, GraceHandler)

        if heuristic is None:
            heuristic = DistanceHeuristic()
        assert isinstance(heuristic, Heuristic)

        if job_handler is None:
            job_handler = SerialJobHandler()
        assert isinstance(job_handler, JobHandler)

        if attack_point_optimizer is None:
            attack_point_optimizer = NaiveAttackPointOptimizer()
        assert isinstance(attack_point_optimizer, AttackPointOptimizer)
        if isinstance(self, BeatwiseQTarget) and isinstance(
            attack_point_optimizer, MeasurewiseAttackPointOptimizer
        ):
            message = "{} is not supposed to be used together with {}.".format(
                self.__class__.__name__, attack_point_optimizer.__class__.__name__
            )
            raise TypeError(message)

        # TODO: this step seems unnecessary now (23/09/2021), (maybe) write more tests to verify

        # if next-to-last QEvent is silent, pop the TerminalQEvent,
        # in order to prevent rest-tuplets
        # q_events = q_event_sequence
        # if isinstance(q_event_sequence[-2], SilentQEvent):
        #     q_events = q_event_sequence[:-1]

        # parcel QEvents out to each beat
        beats = self.beats
        offsets = sorted([beat.offset_in_ms for beat in beats])
        for q_event in q_event_sequence:
            index = bisect.bisect(offsets, q_event.offset) - 1
            beat = beats[index]
            beat.q_events.append(q_event)

        # generate QuantizationJobs and process with the JobHandler
        jobs = [beat(i) for i, beat in enumerate(beats)]
        jobs = [job for job in jobs if job]
        jobs = job_handler(jobs)
        for job in jobs:
            assert job is not None
            beats[job.job_id]._q_grids = job.q_grids

        # for i, beat in enumerate(beats):
        #    print i, len(beat.q_grids)
        #    for q_event in beat.q_events:
        #        print '\t{}'.format(q_event.offset)

        # select the best QGrid for each beat, according to the Heuristic
        beats = heuristic(beats)

        # shift QEvents attached to each QGrid's "next downbeat"
        # over to the next QGrid's first leaf - the real downbeat
        orphaned_q_events_proxies = self._shift_downbeat_q_events_to_next_q_grid()

        #  TODO: handle a final QGrid with QEvents attached to its
        #        next_downbeat.
        #  TODO: remove a final QGrid with no QEvents

        self._regroup_q_grid_with_unnecessary_divisions()

        # convert the QGrid representation into notation,
        # handling grace-note behavior with the GraceHandler
        notation = self._notate(
            attach_tempos=attach_tempos,
            attack_point_optimizer=attack_point_optimizer,
            grace_handler=grace_handler,
        )

        handle_orphaned_q_events = getattr(
            grace_handler, "handle_orphaned_q_event_proxies", None
        )
        if callable(handle_orphaned_q_events) and orphaned_q_events_proxies:
            last_leaf = abjad.get.leaf(notation, -1)
            handle_orphaned_q_events(last_leaf, orphaned_q_events_proxies)

        return notation

    ### PRIVATE METHODS ###

    def _attach_attachments_to_logical_ties(
        self,
        voice: abjad.Voice,
        all_attachments: typing.Sequence[tuple | None],
    ):
        logical_tie_list = list(
            abjad.iterate.logical_ties(voice, grace=False, pitched=True)
        )
        assert len(logical_tie_list) == len(all_attachments)
        for logical_tie, attachments in zip(logical_tie_list, all_attachments):
            first_leaf = abjad.get.leaf(logical_tie, 0)
            abjad.annotate(first_leaf, "q_event_attachments", attachments)

    @abc.abstractmethod
    def _notate(
        self,
        grace_handler: GraceHandler,
        attack_point_optimizer: AttackPointOptimizer,
        attach_tempos: bool = True,
    ) -> abjad.Voice:
        raise NotImplementedError

    def _notate_leaves(
        self, grace_handler: GraceHandler, voice: abjad.Voice | None = None
    ) -> list[tuple | None]:
        all_q_event_attachments: list[tuple | None] = []
        for leaf in abjad.iterate.leaves(voice):
            if leaf._has_indicator(dict):
                annotation = leaf._get_indicator(dict)
                q_events = annotation["q_events"]
                pitches, attachments, grace_container = grace_handler(q_events)
                new_leaf: abjad.Leaf
                if not pitches:
                    new_leaf = abjad.Rest(leaf)
                elif 1 < len(pitches):
                    new_leaf = abjad.Chord(leaf)
                    new_leaf.written_pitches = pitches
                else:
                    new_leaf = abjad.Note(leaf)
                    new_leaf.written_pitch = pitches[0]
                if attachments is not None:
                    all_q_event_attachments.append(attachments)
                if grace_container:
                    abjad.attach(grace_container, new_leaf)
                abjad.mutate.replace(leaf, new_leaf)
                if not isinstance(new_leaf, abjad.Rest):
                    abjad.annotate(new_leaf, "tie_to_next", True)
                elif abjad.get.indicator(new_leaf, abjad.Tie):
                    abjad.detach(abjad.Tie, new_leaf)
            else:
                previous_leaf = abjad._iterlib._get_leaf(leaf, -1)
                if isinstance(previous_leaf, abjad.Rest):
                    new_leaf = type(previous_leaf)(leaf.written_duration)
                elif isinstance(previous_leaf, abjad.Note):
                    new_leaf = type(previous_leaf)(
                        previous_leaf.written_pitch, leaf.written_duration
                    )
                else:
                    new_leaf = type(previous_leaf)(
                        previous_leaf.written_pitches, leaf.written_duration
                    )
                abjad.mutate.replace(leaf, new_leaf)
                if abjad.get.annotation(previous_leaf, "tie_to_next") is True:
                    leaves = [previous_leaf, new_leaf]
                    abjad.tie(leaves)
                    abjad.annotate(new_leaf, "tie_to_next", True)
            if leaf._has_indicator(abjad.MetronomeMark):
                tempo = leaf._get_indicator(abjad.MetronomeMark)
                abjad.detach(abjad.MetronomeMark, leaf)
                abjad.detach(abjad.MetronomeMark, new_leaf)
                abjad.attach(tempo, new_leaf)
            if leaf._has_indicator(abjad.TimeSignature):
                time_signature = leaf._get_indicator(abjad.TimeSignature)
                abjad.detach(abjad.TimeSignature, leaf)
                abjad.detach(abjad.TimeSignature, new_leaf)
                abjad.attach(time_signature, new_leaf)
        return all_q_event_attachments

    def _regroup_q_grid_with_unnecessary_divisions(self):
        for beat in self.beats:
            beat.q_grid.regroup_leaves_with_unencessary_divisions()

    def _shift_downbeat_q_events_to_next_q_grid(self) -> list[QEventProxy]:
        beats = self.beats
        assert beats[-1].q_grid is not None
        for one, two in abjad.sequence.nwise(beats):
            one_q_events = one.q_grid.next_downbeat.q_event_proxies
            two_q_events = two.q_grid.leaves[0].q_event_proxies
            while one_q_events:
                two_q_events.insert(0, one_q_events.pop())
        return [
            proxy
            for proxy in beats[-1].q_grid.next_downbeat.q_event_proxies
            if not isinstance(proxy.q_event, TerminalQEvent)
        ]

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def beats(self) -> tuple[QTargetBeat, ...]:
        """
        Beats of q-target.
        """
        raise NotImplementedError

    @property
    def duration_in_ms(self) -> abjad.Duration:
        """
        Duration of q-target in milliseconds.
        """
        last_item = self._items[-1]
        return last_item.offset_in_ms + last_item.duration_in_ms

    @abc.abstractproperty
    def item_class(self):
        """
        Item class of q-target.
        """
        raise NotImplementedError

    @property
    def items(self):
        """
        Items of q-target.
        """
        return self._items


class BeatwiseQTarget(QTarget):
    """
    Beatwise q-target.

    Not composer-safe.

    Used internally by the ``quantize`` function.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZATION ###

    def __init__(self, items: typing.Sequence[QTargetBeat] | None = None):
        items = [] if items is None else items
        self._items: typing.Sequence[QTargetBeat]
        super().__init__(items)

    ### PRIVATE METHODS ###

    def _notate(
        self,
        grace_handler: GraceHandler,
        attack_point_optimizer: AttackPointOptimizer,
        attach_tempos: bool = True,
    ) -> abjad.Voice:
        voice = abjad.Voice()
        # generate the first
        beat = self._items[0]
        assert isinstance(beat, QTargetBeat) and beat.q_grid is not None
        components = beat.q_grid(beat.beatspan)
        if attach_tempos:
            attachment_target: abjad.Component = components[0]
            leaves = abjad.select.leaves(attachment_target)
            if isinstance(attachment_target, abjad.Container):
                attachment_target = leaves[0]
            tempo = copy.deepcopy(beat.tempo)
            abjad.attach(tempo, attachment_target)
        voice.extend(components)

        # generate the rest pairwise, comparing tempi
        for beat_one, beat_two in abjad.sequence.nwise(self.items):
            components = beat_two.q_grid(beat_two.beatspan)
            if (beat_two.tempo != beat_one.tempo) and attach_tempos:
                attachment_target = components[0]
                leaves = abjad.select.leaves(attachment_target)
                if isinstance(attachment_target, abjad.Container):
                    attachment_target = leaves[0]
                tempo = copy.deepcopy(beat_two.tempo)
                abjad.attach(tempo, attachment_target)
            voice.extend(components)

        # apply logical ties, pitches, grace containers
        q_events_attachments = self._notate_leaves(
            grace_handler=grace_handler, voice=voice
        )

        # partition logical ties in voice
        attack_point_optimizer(voice)

        if isinstance(grace_handler, ConcatenatingGraceHandler):
            self._attach_attachments_to_logical_ties(voice, q_events_attachments)

        return voice

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self) -> tuple[QTargetBeat, ...]:
        """
        Beats of beatwise q-target.
        """
        return tuple(self._items)

    @property
    def item_class(self) -> type[QTargetBeat]:
        """
        Item class of beatwise q-target.
        """
        return QTargetBeat


class MeasurewiseQTarget(QTarget):
    """
    Measurewise quantization target.

    Not composer-safe.

    Used internally by the ``quantize`` function.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZATION ###

    def __init__(self, items: typing.Sequence[QTargetMeasure] | None = None):
        super().__init__(items)

    ### PRIVATE METHODS ###

    def _notate(
        self,
        grace_handler: GraceHandler,
        attack_point_optimizer: AttackPointOptimizer,
        attach_tempos: bool = True,
    ) -> abjad.Voice:
        voice = abjad.Voice()

        # generate the first
        q_target_measure = self._items[0]
        assert isinstance(q_target_measure, QTargetMeasure)
        time_signature = q_target_measure.time_signature
        measure = abjad.Container()
        for beat in q_target_measure.beats:
            measure.extend(beat.q_grid(beat.beatspan))
        leaf = abjad.get.leaf(measure, 0)
        abjad.attach(time_signature, leaf)
        if attach_tempos:
            tempo = copy.deepcopy(q_target_measure.tempo)
            leaf = abjad.get.leaf(measure, 0)
            abjad.attach(tempo, leaf)
        voice.append(measure)

        # generate the rest pairwise, comparing tempi
        pairs = abjad.sequence.nwise(self.items)
        for q_target_measure_one, q_target_measure_two in pairs:
            measure = abjad.Container()
            for beat in q_target_measure_two.beats:
                measure.extend(beat.q_grid(beat.beatspan))
            if (
                q_target_measure_two.time_signature
                != q_target_measure_one.time_signature
            ):
                time_signature = q_target_measure_two.time_signature
                leaf = abjad.get.leaf(measure, 0)
                abjad.attach(time_signature, leaf)
            if (
                q_target_measure_two.tempo != q_target_measure_one.tempo
            ) and attach_tempos:
                tempo = copy.deepcopy(q_target_measure_two.tempo)
                # abjad.attach(tempo, measure)
                leaf = abjad.get.leaf(measure, 0)
                abjad.attach(tempo, leaf)
            voice.append(measure)

        # apply logical ties, pitches, grace containers
        q_events_attachments = self._notate_leaves(
            grace_handler=grace_handler, voice=voice
        )

        # partition logical ties in each measure
        for index, measure in enumerate(voice):
            if isinstance(attack_point_optimizer, MeasurewiseAttackPointOptimizer):
                # then we need to pass the time signature of each measure
                attack_point_optimizer(measure, self.items[index].time_signature)
            else:
                attack_point_optimizer(measure)

        if isinstance(grace_handler, ConcatenatingGraceHandler):
            self._attach_attachments_to_logical_ties(voice, q_events_attachments)

        return voice

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self) -> tuple[QTargetBeat, ...]:
        """
        Beats of measurewise q-target.
        """
        return tuple([beat for item in self.items for beat in item.beats])

    @property
    def item_class(self) -> type[QTargetMeasure]:
        """
        Item class of measurewise q-target.
        """
        return QTargetMeasure
