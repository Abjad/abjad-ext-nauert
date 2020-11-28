from .QEvent import QEvent


class TerminalQEvent(QEvent):
    """
    Terminal q-event.

    ..  container:: example

        >>> q_event = abjadext.nauert.TerminalQEvent(1000)
        >>> string = format(q_event)
        >>> print(string)
        abjadext.nauert.TerminalQEvent(
            offset=abjad.Offset((1000, 1)),
            )

    Carries no significance outside the context of a ``QEventSequence``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_offset",)

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, offset=0):
        QEvent.__init__(self, offset=offset)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when `argument` is a terminal q-event with offset equal to that
        of this terminal q-event. Otherwise false.
        """
        if type(self) == type(argument) and self.offset == argument.offset:
            return True
        return False

    def __hash__(self) -> int:
        """
        Hashes terminal q-event.

        Required to be explicitly redefined on Python 3 if __eq__ changes.
        """
        return super(TerminalQEvent, self).__hash__()
