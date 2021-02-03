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
from .qevents import SilentQEvent
from .qeventsequence import QEventSequence
from .qtargetitems import QTargetBeat, QTargetMeasure


class QTarget:
    """
    Abstract q-target.

    ``QTarget`` is created by a concrete ``QSchema`` instance, and represents
    the mold into which the timepoints contained by a ``QSequence`` instance
    will be poured, as structured by that ``QSchema`` instance.

    Not composer-safe.

    Used internally by the ``Quantizer``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_items",)

    ### INITIALIZATION ###

    def __init__(self, items=None):
        items = items or []
        assert all(isinstance(x, self.item_class) for x in items)
        self._items = tuple(sorted(items, key=lambda x: x.offset_in_ms))

    ### SPECIAL METHODS ###

    def __call__(
        self,
        q_event_sequence,
        grace_handler=None,
        heuristic=None,
        job_handler=None,
        attack_point_optimizer=None,
        attach_tempos=True,
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

        # if next-to-last QEvent is silent, pop the TerminalQEvent,
        # in order to prevent rest-tuplets
        q_events = q_event_sequence
        if isinstance(q_event_sequence[-2], SilentQEvent):
            q_events = q_event_sequence[:-1]

        # parcel QEvents out to each beat
        beats = self.beats
        offsets = sorted([beat.offset_in_ms for beat in beats])
        for q_event in q_events:
            index = bisect.bisect(offsets, q_event.offset) - 1
            beat = beats[index]
            beat.q_events.append(q_event)

        # generate QuantizationJobs and process with the JobHandler
        jobs = [beat(i) for i, beat in enumerate(beats)]
        jobs = [job for job in jobs if job]
        jobs = job_handler(jobs)
        for job in jobs:
            beats[job.job_id]._q_grids = job.q_grids

        # for i, beat in enumerate(beats):
        #    print i, len(beat.q_grids)
        #    for q_event in beat.q_events:
        #        print '\t{}'.format(q_event.offset)

        # select the best QGrid for each beat, according to the Heuristic
        beats = heuristic(beats)

        # shift QEvents attached to each QGrid's "next downbeat"
        # over to the next QGrid's first leaf - the real downbeat
        self._shift_downbeat_q_events_to_next_q_grid()

        #  TODO: handle a final QGrid with QEvents attached to its
        #        next_downbeat.
        #  TODO: remove a final QGrid with no QEvents

        # convert the QGrid representation into notation,
        # handling grace-note behavior with the GraceHandler
        return self._notate(
            attach_tempos=attach_tempos,
            attack_point_optimizer=attack_point_optimizer,
            grace_handler=grace_handler,
        )

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _notate(
        self,
        grace_handler=None,
        attack_point_optimizer=None,
        attach_tempos=True,
    ):
        pass

    def _notate_leaves(self, grace_handler=None, voice=None):
        for leaf in abjad.iterate(voice).leaves():
            if leaf._has_indicator(dict):
                annotation = leaf._get_indicator(dict)
                q_events = annotation["q_events"]
                pitches, grace_container = grace_handler(q_events)
                if not pitches:
                    new_leaf = abjad.Rest(leaf)
                elif 1 < len(pitches):
                    new_leaf = abjad.Chord(leaf)
                    new_leaf.written_pitches = pitches
                else:
                    new_leaf = abjad.Note(leaf)
                    new_leaf.written_pitch = pitches[0]
                if grace_container:
                    abjad.attach(grace_container, new_leaf)
                abjad.mutate.replace(leaf, new_leaf)
                if not isinstance(new_leaf, abjad.Rest):
                    abjad.annotate(new_leaf, "tie_to_next", True)
            else:
                previous_leaf = abjad._iterate._get_leaf(leaf, -1)
                if isinstance(previous_leaf, abjad.Rest):
                    new_leaf = type(previous_leaf)(leaf.written_duration)
                elif isinstance(previous_leaf, abjad.Note):
                    new_leaf = type(previous_leaf)(
                        previous_leaf.written_pitch, leaf.written_duration
                    )
                else:
                    new_leaf = type(previous_leaf)(
                        previous_leaf.written_pitch, leaf.written_duration
                    )
                abjad.mutate.replace(leaf, new_leaf)
                if abjad.get.annotation(previous_leaf, "tie_to_next") is True:
                    leaves = abjad.select([previous_leaf, new_leaf])
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

    def _shift_downbeat_q_events_to_next_q_grid(self):
        beats = self.beats
        for one, two in abjad.sequence(beats).nwise():
            one_q_events = one.q_grid.next_downbeat.q_event_proxies
            two_q_events = two.q_grid.leaves[0].q_event_proxies
            while one_q_events:
                two_q_events.append(one_q_events.pop())

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def beats(self):
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

    Used internally by ``Quantizer``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _notate(
        self,
        attach_tempos=True,
        attack_point_optimizer=None,
        grace_handler=None,
    ):
        voice = abjad.Voice()
        # generate the first
        beat = self.items[0]
        components = beat.q_grid(beat.beatspan)
        if attach_tempos:
            attachment_target = components[0]
            leaves = abjad.select(attachment_target).leaves()
            if isinstance(attachment_target, abjad.Container):
                attachment_target = leaves[0]
            tempo = copy.deepcopy(beat.tempo)
            abjad.attach(tempo, attachment_target)
        voice.extend(components)

        # generate the rest pairwise, comparing tempi
        for beat_one, beat_two in abjad.sequence(self.items).nwise():
            components = beat_two.q_grid(beat_two.beatspan)
            if (beat_two.tempo != beat_one.tempo) and attach_tempos:
                attachment_target = components[0]
                leaves = abjad.select(attachment_target).leaves()
                if isinstance(attachment_target, abjad.Container):
                    attachment_target = leaves[0]
                tempo = copy.deepcopy(beat_two.tempo)
                abjad.attach(tempo, attachment_target)
            voice.extend(components)

        # apply logical ties, pitches, grace containers
        self._notate_leaves(grace_handler=grace_handler, voice=voice)

        # partition logical ties in voice
        attack_point_optimizer(voice)

        return voice

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self):
        """
        Beats of beatwise q-target.
        """
        return tuple(self.items)

    @property
    def item_class(self) -> typing.Type[QTargetBeat]:
        """
        Item class of beatwise q-target.
        """
        return QTargetBeat


class MeasurewiseQTarget(QTarget):
    """
    Measurewise quantization target.

    Not composer-safe.

    Used internally by ``Quantizer``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _notate(
        self,
        attach_tempos=True,
        attack_point_optimizer=None,
        grace_handler=None,
    ):
        voice = abjad.Voice()

        # generate the first
        q_target_measure = self.items[0]
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
        pairs = abjad.sequence(self.items).nwise()
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
        self._notate_leaves(grace_handler=grace_handler, voice=voice)

        # partition logical ties in each measure
        for index, measure in enumerate(voice):
            if isinstance(attack_point_optimizer, MeasurewiseAttackPointOptimizer):
                # then we need to pass the time signature of each measure
                attack_point_optimizer(measure, self.items[index].time_signature)
            else:
                attack_point_optimizer(measure)

        return voice

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self) -> typing.Tuple:
        """
        Beats of measurewise q-target.
        """
        return tuple([beat for item in self.items for beat in item.beats])

    @property
    def item_class(self) -> typing.Type[QTargetMeasure]:
        """
        Item class of measurewise q-target.
        """
        return QTargetMeasure
