from .AttackPointOptimizer import AttackPointOptimizer


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
