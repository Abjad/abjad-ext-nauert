from abjadext.nauert.GraceHandler import GraceHandler


class CollapsingGraceHandler(GraceHandler):
    r'''Collapsing grace-handler.

    Collapses pitch information into a single chord rather than creating a
    grace container.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        r'''Calls collapsing grace handler.
        '''
        import abjadext.nauert
        pitches = []
        for q_event in q_events:
            if isinstance(q_event, abjadext.nauert.PitchedQEvent):
                pitches.extend(q_event.pitches)
        return tuple(pitches), None
