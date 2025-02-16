import abjad

from . import attackpointoptimizers as _attackpointoptimizers
from . import gracehandlers as _gracehandlers
from . import heuristics as _heuristics
from . import jobhandlers as _jobhandlers
from . import qeventsequence as _qeventsequence
from . import qschemas as _qschemas


def quantize(
    q_event_sequence: _qeventsequence.QEventSequence,
    q_schema: _qschemas.QSchema | None = None,
    grace_handler: _gracehandlers.GraceHandler | None = None,
    heuristic: _heuristics.Heuristic | None = None,
    job_handler: _jobhandlers.JobHandler | None = None,
    attack_point_optimizer: _attackpointoptimizers.AttackPointOptimizer | None = None,
    attach_tempos: bool = True,
) -> abjad.Voice:
    r"""
    Quantizer function.

    Quantizes sequences of attack-points, encapsulated by ``QEventSequences``,
    into score trees.

    ..  container:: example

        >>> durations = [1000] * 8
        >>> pitches = range(8)
        >>> pairs = tuple(zip(durations, pitches, strict=True))
        >>> method = nauert.QEventSequence.from_millisecond_pitch_pairs
        >>> q_event_sequence = method(pairs)

    ..  container:: example

        Quantization defaults to outputting into a 4/4, quarter=60 musical structure:

        >>> result = nauert.quantize(q_event_sequence)
        >>> staff = abjad.Staff([result])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \new Voice
                    {
                        {
                            \tempo 4=60
                            \time 4/4
                            c'4
                            cs'4
                            d'4
                            ef'4
                        }
                        {
                            e'4
                            f'4
                            fs'4
                            g'4
                        }
                    }
                }
            >>

    ..  container:: example

        However, the behavior of the ``quantize`` function can be modified at
        call-time. Passing a ``QSchema`` instance will alter the
        macro-structure of the output.

        Here, we quantize using settings specified by a ``MeasurewiseQSchema``,
        which will cause the ``quantize`` function to group the output into
        measures with different tempi and time signatures:

        >>> measurewise_q_schema = nauert.MeasurewiseQSchema(
        ...     {
        ...         "tempo": abjad.MetronomeMark(abjad.Duration(1, 4), 78),
        ...         "time_signature": abjad.TimeSignature((2, 4)),
        ...     },
        ...     {
        ...         "tempo": abjad.MetronomeMark(abjad.Duration(1, 8), 57),
        ...         "time_signature": abjad.TimeSignature((5, 4)),
        ...     },
        ... )
        >>> result = nauert.quantize(
        ...     q_event_sequence,
        ...     q_schema=measurewise_q_schema,
        ... )
        >>> staff = abjad.Staff([result])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \new Voice
                    {
                        {
                            \tempo 4=78
                            \time 2/4
                            c'4
                            ~
                            \tuplet 5/4 {
                                c'16.
                                cs'8..
                                ~
                            }
                        }
                        {
                            \tuplet 7/4 {
                                \tempo 8=57
                                \time 5/4
                                cs'16.
                                d'8
                                ~
                            }
                            \tuplet 5/4 {
                                d'16
                                ef'16.
                                ~
                            }
                            \tuplet 3/2 {
                                ef'16
                                e'8
                                ~
                            }
                            \tuplet 7/4 {
                                e'16
                                f'8
                                ~
                                f'32
                                ~
                            }
                            f'32
                            fs'16.
                            ~
                            \tuplet 5/4 {
                                fs'32
                                g'8
                                ~
                            }
                            \tuplet 7/4 {
                                g'32
                                r32
                                r16
                                r16
                                r16
                                r16
                                r16
                                r16
                            }
                            r4
                        }
                    }
                }
            >>

    ..  container:: example

        Here we quantize using settings specified by a ``BeatwiseQSchema``,
        which keeps the output of the ``quantize`` function "flattened",
        without measures or explicit time signatures.  The default beat-wise
        settings of quarter=60 persists until the third "beatspan":

        >>> beatwise_q_schema = nauert.BeatwiseQSchema(
        ... {
        ...     2: {"tempo": abjad.MetronomeMark(abjad.Duration(1, 4), 120)},
        ...     5: {"tempo": abjad.MetronomeMark(abjad.Duration(1, 4), 90)},
        ...     7: {"tempo": abjad.MetronomeMark(abjad.Duration(1, 4), 30)},
        ... })

        >>> result = nauert.quantize(
        ...     q_event_sequence,
        ...     q_schema=beatwise_q_schema,
        ... )
        >>> staff = abjad.Staff([result])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \new Voice
                    {
                        \tempo 4=60
                        c'4
                        cs'4
                        \tempo 4=120
                        d'2
                        ef'4
                        ~
                        \tempo 4=90
                        ef'8.
                        e'4
                        ~
                        e'16
                        ~
                        \tuplet 3/2 {
                            \tempo 4=30
                            e'32
                            f'8.
                            fs'8
                            ~
                            fs'32
                            ~
                        }
                        \tuplet 3/2 {
                            fs'32
                            g'8.
                            r32
                            r8
                        }
                    }
                }
            >>

        Note that ``TieChains`` are generally fused together in the above
        example, but break at tempo changes.

    ..  container::

        The use of `BeatwiseQSchema` and `MeasurewiseAttackPointOptimizer` is
        not supported. Please raise an issue if you would like this to be
        supported in the future.

        >>> q_schema = nauert.BeatwiseQSchema()
        >>> attack_point_optimizer = nauert.MeasurewiseAttackPointOptimizer()
        >>> result = nauert.quantize(
        ...     q_event_sequence,
        ...     attack_point_optimizer=attack_point_optimizer,
        ...     q_schema=q_schema,
        ... )
        Traceback (most recent call last):
            ...
        TypeError: BeatwiseQTarget is not ... with MeasurewiseAttackPointOptimizer.

    Other keyword arguments are:

        * ``grace_handler``: a ``GraceHandler`` instance controls whether and
          how grace notes are used in the output.  Options currently include
          ``CollapsingGraceHandler``, ``ConcatenatingGraceHandler`` and
          ``DiscardingGraceHandler``.

        * ``heuristic``: a ``Heuristic`` instance controls how output rhythms
          are selected from a pool of candidates.  Options currently include
          the ``DistanceHeuristic`` class.

        * ``job_handler``: a ``JobHandler`` instance controls whether or not
          parallel processing is used during the quantization process.
          Options include the ``SerialJobHandler`` and ``ParallelJobHandler``
          classes.

        * ``attack_point_optimizer``: an ``AttackPointOptimizer`` instance
          controls whether and how logical ties are re-notated.
          Options currently include ``MeasurewiseAttackPointOptimizer``,
          ``NaiveAttackPointOptimizer`` and ``NullAttackPointOptimizer``.

    Refer to the reference pages for ``BeatwiseQSchema`` and
    ``MeasurewiseQSchema`` for more information on controlling the ``quantize``
    function's output, and to the reference on ``SearchTree`` for information
    on controlling the rhythmic complexity of that same output.
    """
    # TODO: assert isinstance(q_event_sequence, QEventSequence)
    q_event_sequence = _qeventsequence.QEventSequence(q_event_sequence)
    if q_schema is None:
        q_schema = _qschemas.MeasurewiseQSchema()
    assert isinstance(q_schema, _qschemas.QSchema)
    q_target = q_schema(q_event_sequence.duration_in_ms)
    notation = q_target(
        q_event_sequence,
        grace_handler=grace_handler,
        heuristic=heuristic,
        job_handler=job_handler,
        attack_point_optimizer=attack_point_optimizer,
        attach_tempos=attach_tempos,
    )
    return notation
