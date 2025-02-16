import abc

import abjad


class AttackPointOptimizer(abc.ABC):
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
        """
        Calls attack-point optimizer.
        """
        raise NotImplementedError


class MeasurewiseAttackPointOptimizer(AttackPointOptimizer):
    r"""
    Measurewise attack-point optimizer.

    Attempts to optimize attack points in an expression with regard to the
    effective time signature of that expression.

    Only acts on measures.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> source_tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> q_events = nauert.QEventSequence.from_tempo_scaled_leaves(
        ...     staff[:],
        ...     tempo=source_tempo,
        ... )
        >>> target_tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 54)
        >>> q_schema = nauert.MeasurewiseQSchema(tempo=target_tempo)

    ..  container:: example

        Without the measure-wise attack-point optimizer:

        >>> voice = nauert.quantize(q_events, q_schema=q_schema)
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=54
                    \time 4/4
                    c'16..
                    d'64
                    ~
                    \tuplet 5/4
                    {
                        d'8
                        e'32
                        ~
                    }
                    \tuplet 7/4
                    {
                        e'8
                        ~
                        e'32
                        f'16
                        ~
                    }
                    \tuplet 5/4
                    {
                        f'16.
                        g'16
                        ~
                    }
                    g'16
                    a'16
                    ~
                    \tuplet 5/4
                    {
                        a'16
                        b'16.
                        ~
                    }
                    \tuplet 7/4
                    {
                        b'16
                        c''8
                        ~
                        c''32
                        ~
                    }
                    \tuplet 5/4
                    {
                        c''32
                        r32
                        r32
                        r32
                        r32
                    }
                }
            }

    ..  container:: example

        With the measure-wise attack-point optimizer:

        >>> optimizer = nauert.MeasurewiseAttackPointOptimizer()
        >>> voice = nauert.quantize(
        ...     q_events,
        ...     attack_point_optimizer=optimizer,
        ...     q_schema=q_schema,
        ... )
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=54
                    \time 4/4
                    c'16..
                    d'64
                    ~
                    \tuplet 5/4
                    {
                        d'16.
                        ~
                        d'32
                        e'32
                        ~
                    }
                    \tuplet 7/4
                    {
                        e'16.
                        ~
                        e'16
                        f'16
                        ~
                    }
                    \tuplet 5/4
                    {
                        f'16.
                        g'16
                        ~
                    }
                    g'16
                    a'16
                    ~
                    \tuplet 5/4
                    {
                        a'16
                        b'32
                        ~
                        b'16
                        ~
                    }
                    \tuplet 7/4
                    {
                        b'16
                        c''32
                        ~
                        c''8
                        ~
                    }
                    \tuplet 5/4
                    {
                        c''32
                        r16
                        r16
                    }
                }
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(
        self,
        argument: abjad.Container,
        time_signature: abjad.TimeSignature | None = None,
    ) -> None:
        """
        Calls measurewise attack-point optimizer.
        """
        assert isinstance(argument, abjad.Container)
        if time_signature is None:
            leaf = abjad.get.leaf(argument, 0)
            time_signature = abjad.get.indicator(leaf, abjad.TimeSignature)
        assert isinstance(time_signature, abjad.TimeSignature), repr(time_signature)
        all_annotations = self._get_attachment_annotations_of_logical_ties(argument[:])
        rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
        meter = abjad.Meter(rtc)
        meter.rewrite(argument[:], boundary_depth=1)
        plts = list(abjad.iterate.logical_ties(argument[:], pitched=True))
        assert len(all_annotations) == len(plts)
        self._reannotate_logical_ties(argument[:], all_annotations)

    @staticmethod
    def _get_attachment_annotations_of_logical_ties(components):
        all_annotations = []
        for plt in abjad.iterate.logical_ties(components, pitched=True):
            first_leaf = abjad.get.leaf(plt, 0)
            annotation = abjad.get.annotation(first_leaf, "q_event_attachments")
            all_annotations.append(annotation)
        return all_annotations

    @staticmethod
    def _reannotate_logical_ties(components, all_annotations):
        plts = abjad.iterate.logical_ties(components, pitched=True)
        for plt, annotation in zip(plts, all_annotations, strict=True):
            leaf = abjad.get.leaf(plt, 0)
            abjad.annotate(leaf, "q_event_attachments", annotation)


class NaiveAttackPointOptimizer(AttackPointOptimizer):
    r"""
    Naive attack-point optimizer. (The default attack-point optimizer)

    Optimizes attack points by fusing tie leaves within logical ties with leaf
    durations decreasing monotonically.

    Logical ties will be partitioned into sub-logical-ties if leaves are found
    with metronome marks attached.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> source_tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> q_events = nauert.QEventSequence.from_tempo_scaled_leaves(
        ...     staff[:],
        ...     tempo=source_tempo,
        ... )
        >>> target_tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 54)
        >>> q_schema = nauert.MeasurewiseQSchema(tempo=target_tempo)

    ..  container:: example

        >>> optimizer = nauert.NaiveAttackPointOptimizer()
        >>> voice = nauert.quantize(
        ...     q_events,
        ...     attack_point_optimizer=optimizer,
        ...     q_schema=q_schema,
        ... )
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=54
                    \time 4/4
                    c'16..
                    d'64
                    ~
                    \tuplet 5/4
                    {
                        d'8
                        e'32
                        ~
                    }
                    \tuplet 7/4
                    {
                        e'8
                        ~
                        e'32
                        f'16
                        ~
                    }
                    \tuplet 5/4
                    {
                        f'16.
                        g'16
                        ~
                    }
                    g'16
                    a'16
                    ~
                    \tuplet 5/4
                    {
                        a'16
                        b'16.
                        ~
                    }
                    \tuplet 7/4
                    {
                        b'16
                        c''8
                        ~
                        c''32
                        ~
                    }
                    \tuplet 5/4
                    {
                        c''32
                        r32
                        r32
                        r32
                        r32
                    }
                }
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls naive attack-point optimizer.
        """
        lts = abjad.iterate.logical_ties(argument, grace=False, reverse=True)
        for lt in lts:
            sub_logical_ties = []
            current_sub_logical_tie = []
            for leaf in lt:
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
    r"""
    Null attack-point optimizer.

    Performs no attack-point optimization.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> source_tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
        >>> q_events = nauert.QEventSequence.from_tempo_scaled_leaves(
        ...     staff[:],
        ...     tempo=source_tempo,
        ... )
        >>> target_tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 54)
        >>> q_schema = nauert.MeasurewiseQSchema(tempo=target_tempo)

    ..  container:: example

        >>> optimizer = nauert.NullAttackPointOptimizer()
        >>> voice = nauert.quantize(
        ...     q_events,
        ...     attack_point_optimizer=optimizer,
        ...     q_schema=q_schema,
        ... )
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=54
                    \time 4/4
                    c'16
                    ~
                    c'32
                    ~
                    c'64
                    d'64
                    ~
                    \tuplet 5/4
                    {
                        d'32
                        ~
                        d'32
                        ~
                        d'32
                        ~
                        d'32
                        e'32
                        ~
                    }
                    \tuplet 7/4
                    {
                        e'32
                        ~
                        e'32
                        ~
                        e'32
                        ~
                        e'32
                        ~
                        e'32
                        f'32
                        ~
                        f'32
                        ~
                    }
                    \tuplet 5/4
                    {
                        f'32
                        ~
                        f'32
                        ~
                        f'32
                        g'32
                        ~
                        g'32
                        ~
                    }
                    g'16
                    a'16
                    ~
                    \tuplet 5/4
                    {
                        a'32
                        ~
                        a'32
                        b'32
                        ~
                        b'32
                        ~
                        b'32
                        ~
                    }
                    \tuplet 7/4
                    {
                        b'32
                        ~
                        b'32
                        c''32
                        ~
                        c''32
                        ~
                        c''32
                        ~
                        c''32
                        ~
                        c''32
                        ~
                    }
                    \tuplet 5/4
                    {
                        c''32
                        r32
                        r32
                        r32
                        r32
                    }
                }
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls null attack-point optimizer.
        """
        pass
