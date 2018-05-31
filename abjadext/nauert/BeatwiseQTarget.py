import abjad
import copy
from abjadext.nauert.QTarget import QTarget


class BeatwiseQTarget(QTarget):
    r'''Beatwise q-target.

    Not composer-safe.

    Used internally by ``Quantizer``.
    '''

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
        self._notate_leaves(
            grace_handler=grace_handler,
            voice=voice,
            )

        # partition logical ties in voice
        attack_point_optimizer(voice)

        return voice

    ### PUBLIC PROPERTIES ###

    @property
    def beats(self):
        r'''Beats of beatwise q-target.
        '''
        return tuple(self.items)

    @property
    def item_class(self):
        r'''Item class of beatwise q-target.
        '''
        import abjadext
        return abjadext.nauert.QTargetBeat
