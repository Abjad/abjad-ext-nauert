import abjad
from abjadext.nauert.QGridLeaf import QGridLeaf


class QGridContainer(abjad.rhythmtrees.RhythmTreeContainer):
    r'''Q-grid container.

    ..  container:: example

        >>> container = abjadext.nauert.QGridContainer()
        >>> abjad.f(container)
        abjadext.nauert.QGridContainer(
            children=(),
            preprolated_duration=abjad.Duration(1, 1),
            )

    Used internally by ``QGrid``.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def leaves(self):
        '''
        Get leaves.
        '''
        return tuple(
            _ for _ in self.depth_first()
            if isinstance(_, QGridLeaf)
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _leaf_class(self):
        import abjadext.nauert
        return abjadext.nauert.QGridLeaf

    @property
    def _node_class(self):
        import abjadext.nauert
        return (type(self), abjadext.nauert.QGridLeaf)
