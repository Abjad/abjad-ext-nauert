import abc

from .qgrid import QGrid
from .qtargetitems import QTargetBeat


class Heuristic:
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

    def __call__(self, q_target_beats) -> None:
        """
        Calls heuristic.
        """
        assert len(q_target_beats)
        assert all(isinstance(x, QTargetBeat) for x in q_target_beats)
        return self._process(q_target_beats)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _process(self, q_target_beats):
        raise NotImplementedError


class DistanceHeuristic(Heuristic):
    """
    Distance heuristic.

    Considers only the computed distance of each ``QGrid`` and the number of
    leaves of that ``QGrid`` when choosing the optimal ``QGrid`` for a given
    ``QTargetBeat``.

    The ``QGrid`` with the smallest distance and fewest number of
    leaves will be selected.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _process(self, q_target_beats):
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
