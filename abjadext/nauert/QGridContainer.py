import abjad

from .QGridLeaf import QGridLeaf


class QGridContainer(abjad.rhythmtrees.RhythmTreeContainer):
    """
    Q-grid container.

    ..  container:: example

        >>> container = abjadext.nauert.QGridContainer()
        >>> abjad.f(container)
        abjadext.nauert.QGridContainer(
            children=(),
            preprolated_duration=abjad.Duration(1, 1),
            )

    Used internally by ``QGrid``.
    """

    ### PUBLIC PROPERTIES ###

    @property
    def leaves(self):
        """
        Get leaves.
        """
        return tuple(_ for _ in self.depth_first() if isinstance(_, QGridLeaf))

    ### PRIVATE PROPERTIES ###

    @property
    def _leaf_class(self):
        return QGridLeaf

    @property
    def _node_class(self):
        return (type(self), QGridLeaf)
