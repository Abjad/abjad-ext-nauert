import abc
import abjad


class Heuristic(abjad.AbjadObject):
    r'''Abstract heuristic.

    Heuristics rank Q-grids according to the criteria they encapsulate.

    They provide the means by which the quantizer selects a single ``QGrid``
    from all computed ``QGrids`` for any given ``QTargetBeat`` to
    represent that beat.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, q_target_beats):
        r'''Calls heuristic.

        Returns none.
        '''
        import abjadext.nauert
        assert len(q_target_beats)
        assert all(isinstance(x, abjadext.nauert.QTargetBeat)
            for x in q_target_beats)
        return self._process(q_target_beats)

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _process(self, q_target_beats):
        raise NotImplementedError
