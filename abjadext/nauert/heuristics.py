import abc

from . import qgrid as _qgrid
from . import qtargetitems as _qtargetitems


class Heuristic(abc.ABC):
    """
    Abstract heuristic.

    Heuristics rank Q-grids according to the criteria they encapsulate.

    Heuristics provide the means by which the quantizer selects a single
    ``QGrid`` from all computed ``QGrids`` for any given ``QTargetBeat`` to
    represent that beat.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(
        self, q_target_beats: tuple[_qtargetitems.QTargetBeat, ...]
    ) -> tuple[_qtargetitems.QTargetBeat, ...]:
        """
        Calls heuristic.
        """
        assert len(q_target_beats)
        assert all(isinstance(x, _qtargetitems.QTargetBeat) for x in q_target_beats)
        return self._process(q_target_beats)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _process(
        self, q_target_beats: tuple[_qtargetitems.QTargetBeat, ...]
    ) -> tuple[_qtargetitems.QTargetBeat, ...]:
        raise NotImplementedError


class DistanceHeuristic(Heuristic):
    r"""
    Distance heuristic.

    Considers only the computed distance of each ``QGrid`` and the number of
    leaves of that ``QGrid`` when choosing the optimal ``QGrid`` for a given
    ``QTargetBeat``.

    The ``QGrid`` with the smallest distance and fewest number of leaves will
    be selected.

    ..  container:: example

        >>> durations = [1000] * 8
        >>> pitches = range(8)
        >>> pairs = tuple(zip(durations, pitches, strict=True))
        >>> q_event_sequence = nauert.QEventSequence.from_millisecond_pitch_pairs(pairs)
        >>> heuristic = nauert.DistanceHeuristic()
        >>> voice = nauert.quantize(q_event_sequence, heuristic=heuristic)
        >>> staff = abjad.Staff([voice])
        >>> score = abjad.Score([staff])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(voice)
            >>> print(string)
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

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _process(
        self, q_target_beats: tuple[_qtargetitems.QTargetBeat, ...]
    ) -> tuple[_qtargetitems.QTargetBeat, ...]:
        for q_target_beat in q_target_beats:
            q_grids = q_target_beat.q_grids
            if q_grids:
                sorted_q_grids = sorted(
                    q_grids, key=lambda x: (x.distance, len(x.leaves))
                )
                q_target_beat._q_grid = sorted_q_grids[0]
            else:
                q_target_beat._q_grid = _qgrid.QGrid()
        return q_target_beats
