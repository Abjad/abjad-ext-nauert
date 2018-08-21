import abjad
import copy
from abjadext.nauert.QTarget import QTarget


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
        leaf = abjad.inspect(measure).leaf(0)
        abjad.attach(time_signature, leaf)
        if attach_tempos:
            tempo = copy.deepcopy(q_target_measure.tempo)
            leaf = abjad.inspect(measure).leaf(0)
            abjad.attach(tempo, leaf)
        voice.append(measure)

        # generate the rest pairwise, comparing tempi
        pairs = abjad.sequence(self.items).nwise()
        for q_target_measure_one, q_target_measure_two in pairs:
            measure = abjad.Container()
            time_signature = q_target_measure_two.time_signature
            for beat in q_target_measure_two.beats:
                measure.extend(beat.q_grid(beat.beatspan))
            leaf = abjad.inspect(measure).leaf(0)
            abjad.attach(time_signature, leaf)
            if ((q_target_measure_two.tempo != q_target_measure_one.tempo) and
                attach_tempos):
                tempo = copy.deepcopy(q_target_measure_two.tempo)
                #abjad.attach(tempo, measure)
                leaf = abjad.inspect(measure).leaf(0)
                abjad.attach(tempo, leaf)
            voice.append(measure)

        # apply logical ties, pitches, grace containers
        self._notate_leaves(
            grace_handler=grace_handler,
            voice=voice,
            )

        # partition logical ties in each measure
        for measure in voice:
            attack_point_optimizer(measure)

        return voice

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self):
        """
        Beats of measurewise q-target.

        Returns tuple.
        """
        return tuple([beat for item in self.items for beat in item.beats])

    @property
    def item_class(self):
        """
        Item class of measurewise q-target.

        Returns q-target measure class.
        """
        import abjadext.nauert
        return abjadext.nauert.QTargetMeasure
