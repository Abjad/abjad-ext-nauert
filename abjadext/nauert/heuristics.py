import abc
import typing

from .qgrid import QGrid
from .qtargetitems import QTargetBeat


class Heuristic(abc.ABC):
    """
    Abstract heuristic.

    Heuristics rank Q-grids according to the criteria they encapsulate.

    They provide the means by which the quantizer selects a single ``QGrid``
    from all computed ``QGrids`` for any given ``QTargetBeat`` to
    represent that beat.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(
        self, q_target_beats: typing.Tuple[QTargetBeat, ...]
    ) -> typing.Tuple[QTargetBeat, ...]:
        """
        Calls heuristic.
        """
        assert len(q_target_beats)
        assert all(isinstance(x, QTargetBeat) for x in q_target_beats)
        return self._process(q_target_beats)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _process(
        self, q_target_beats: typing.Tuple[QTargetBeat, ...]
    ) -> typing.Tuple[QTargetBeat, ...]:
        raise NotImplementedError


class DistanceHeuristic(Heuristic):
    r"""
    Distance heuristic.

    Considers only the computed distance of each ``QGrid`` and the number of
    leaves of that ``QGrid`` when choosing the optimal ``QGrid`` for a given
    ``QTargetBeat``.

    The ``QGrid`` with the smallest distance and fewest number of
    leaves will be selected.

    ..  container:: example

        >>> quantizer = nauert.Quantizer()
        >>> durations = [1000] * 8
        >>> pitches = range(8)
        >>> q_event_sequence = \
        ...     nauert.QEventSequence.from_millisecond_pitch_pairs(
        ...     tuple(zip(durations, pitches)))
        >>> heuristic = nauert.DistanceHeuristic()
        >>> result = quantizer(q_event_sequence, heuristic=heuristic)
        >>> abjad.show(result) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(result)
            >>> print(string)
            \new Voice
            {
                {
                    \tempo 4=60
                    %%% \time 4/4 %%%
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

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _process(
        self, q_target_beats: typing.Tuple[QTargetBeat, ...]
    ) -> typing.Tuple[QTargetBeat, ...]:
        for q_target_beat in q_target_beats:
            q_grids = q_target_beat.q_grids
            if q_grids:
                sorted_q_grids = sorted(
                    q_grids, key=lambda x: (x.distance, len(x.leaves))
                )
                q_target_beat._q_grid = sorted_q_grids[0]
            else:
                q_target_beat._q_grid = QGrid()
        return q_target_beats
