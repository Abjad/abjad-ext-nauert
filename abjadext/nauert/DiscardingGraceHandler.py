from abjadext.nauert.GraceHandler import GraceHandler


class DiscardingGraceHandler(GraceHandler):
    r'''Discarindg grace-handler.

    Dscards all but final q-event attached to an offset.

    Does not create grace containers.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        r'''Calls idscarind grace handler.
        '''
        import abjadext.nauert
        q_event = q_events[-1]
        if isinstance(q_event, abjadext.nauert.PitchedQEvent):
            return q_event.pitches, None
        return (), None
