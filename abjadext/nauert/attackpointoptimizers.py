import abc

import abjad


class AttackPointOptimizer:
    """
    Abstract attack-point optimizer.

    Attack-point optimizers may alter the number, order, and individual
    durations of leaves in a logical tie, but may not alter the overall
    duration of that logical tie.

    They effectively "clean up" notation, post-quantization.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, argument):
        """Calls attack-point optimizer."""
        raise NotImplementedError


class MeasurewiseAttackPointOptimizer(AttackPointOptimizer):
    """
    Measurewise attack-point optimizer.

    Attempts to optimize attack points in an expression with regard to the
    effective time signature of that expression.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> source_tempo = abjad.MetronomeMark((1, 4), 60)
        >>> q_events = abjadext.nauert.QEventSequence.from_tempo_scaled_leaves(
        ...     staff[:],
        ...     tempo=source_tempo,
        ... )
        >>> target_tempo = abjad.MetronomeMark((1, 4), 54)
        >>> q_schema = abjadext.nauert.MeasurewiseQSchema(
        ...     tempo=target_tempo,
        ... )
        >>> quantizer = abjadext.nauert.Quantizer()

    ..  container:: example

        Without the measure-wise attack-point optimizer:

        >>> result = quantizer(
        ...     q_events,
        ...     q_schema=q_schema,
        ... )
        >>> abjad.show(result) # doctest: +SKIP

    ..  container:: example

        With the measure-wise attack-point optimizer:

        >>> optimizer = abjadext.nauert.MeasurewiseAttackPointOptimizer()
        >>> result = quantizer(
        ...     q_events,
        ...     attack_point_optimizer=optimizer,
        ...     q_schema=q_schema,
        ... )
        >>> abjad.show(result) # doctest: +SKIP

    Only acts on measures.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, argument) -> None:
        """
        Calls measurewise attack-point optimizer.
        """
        assert isinstance(argument, abjad.Container)
        leaf = abjad.get.leaf(argument, 0)
        time_signature = abjad.get.indicator(leaf, abjad.TimeSignature)
        assert time_signature is not None, repr(time_signature)
        abjad.Meter.rewrite_meter(argument[:], time_signature, boundary_depth=1)


class NaiveAttackPointOptimizer(AttackPointOptimizer):
    """
    Naive attack-point optimizer.

    Optimizes attack points by fusing tie leaves within logical ties with leaf
    durations decreasing monotonically.

    Logical ties will be partitioned into sub-logical-ties if leaves are found
    with metronome marks attached.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls naive attack-point optimizer.
        """
        for logical_tie in abjad.iterate(argument).logical_ties(
            grace=False, reverse=True
        ):
            sub_logical_ties = []
            current_sub_logical_tie = []
            for leaf in logical_tie:
                tempos = leaf._get_indicators(abjad.MetronomeMark)
                if tempos:
                    if current_sub_logical_tie:
                        current_sub_logical_tie = abjad.LogicalTie(
                            current_sub_logical_tie
                        )
                        sub_logical_ties.append(current_sub_logical_tie)
                    current_sub_logical_tie = []
                current_sub_logical_tie.append(leaf)
            if current_sub_logical_tie:
                current_sub_logical_tie = abjad.LogicalTie(current_sub_logical_tie)
                sub_logical_ties.append(current_sub_logical_tie)
            for sub_logical_tie in sub_logical_ties:
                abjad.mutate._fuse_leaves_by_immediate_parent(sub_logical_tie)


class NullAttackPointOptimizer(AttackPointOptimizer):
    """
    Null attack-point optimizer.

    Performs no attack point optimization.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls null attack-point optimizer.
        """
        pass
