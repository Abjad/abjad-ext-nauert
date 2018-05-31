import abjad
from .AttackPointOptimizer import AttackPointOptimizer


class MeasurewiseAttackPointOptimizer(AttackPointOptimizer):
    r'''Measurewise attack-point optimizer.

    Attempts to optimize attack points in an expression with regard to the
    effective time signature of that expression.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> source_tempo = abjad.MetronomeMark((1, 4), 60)
        >>> q_events = abjadext.nauert.QEventSequence.from_tempo_scaled_leaves(
        ...     staff[:],
        ...     tempo=source_tempo,
        ...     )
        >>> target_tempo = abjad.MetronomeMark((1, 4), 54)
        >>> q_schema = abjadext.nauert.MeasurewiseQSchema(
        ...     tempo=target_tempo,
        ...     )
        >>> quantizer = abjadext.nauert.Quantizer()

    ..  container:: example

        Without the measure-wise attack-point optimizer:

        >>> result = quantizer(
        ...     q_events,
        ...     q_schema=q_schema,
        ...     )
        >>> abjad.show(result) # doctest: +SKIP

    ..  container:: example

        With the measure-wise attack-point optimizer:

        >>> optimizer = abjadext.nauert.MeasurewiseAttackPointOptimizer()
        >>> result = quantizer(
        ...     q_events,
        ...     attack_point_optimizer=optimizer,
        ...     q_schema=q_schema,
        ...     )
        >>> abjad.show(result) # doctest: +SKIP

    Only acts on measures.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r'''Calls measurewise attack-point optimizer.

        Returns none.
        '''
        assert isinstance(argument, abjad.Measure)
        meter = abjad.Meter(argument)
        abjad.mutate(argument[:]).rewrite_meter(
            meter,
            boundary_depth=1,
            )
