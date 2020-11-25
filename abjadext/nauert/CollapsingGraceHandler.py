from .GraceHandler import GraceHandler
from .PitchedQEvent import PitchedQEvent


class CollapsingGraceHandler(GraceHandler):
    """
    Collapsing grace-handler.

    Collapses pitch information into a single chord rather than creating a
    grace container.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, q_events):
        """
        Calls collapsing grace handler.
        """
        pitches = []
        for q_event in q_events:
            if isinstance(q_event, PitchedQEvent):
                pitches.extend(q_event.pitches)
        return tuple(pitches), None
