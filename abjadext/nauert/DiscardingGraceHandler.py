from .GraceHandler import GraceHandler
from .PitchedQEvent import PitchedQEvent


class DiscardingGraceHandler(GraceHandler):
    """
    Discarindg grace-handler.

    Dscards all but final q-event attached to an offset.

    Does not create grace containers.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        """
        Calls discarding grace handler.
        """
        q_event = q_events[-1]
        if isinstance(q_event, PitchedQEvent):
            return q_event.pitches, None
        return (), None
